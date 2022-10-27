import cv2
from pathlib import Path
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label as sk_measure_label
from skimage import filters

import matplotlib.pyplot as plt

from intelligent_placer_lib.cli import parse_args
from intelligent_placer_lib.utils import filter_by_ext


def _show(what, **kw):
    plt.imshow(what, **kw)
    plt.show()


def _pshow(what):
    _show(what, cmap="gray")


def get_largest_component(mask):
    # components are numbered, so 1 1 -> component 1,
    # 2
    # 2 -> component 2 and so on
    labels = sk_measure_label(mask)
    props = regionprops(labels)
    # add max bbox area as well
    *aprops, = filter(lambda e: 1_200_000 > e[1].area > 10_000, enumerate(props))
    [print(p.area, p.bbox) for _, p in aprops]
    _pr = []
    for _, prop in aprops:
        # add diagonal?
        x0, y0, x1, y1 = prop.bbox
        # add the delta checking
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        if max(dx / dy, dy / dx) < 4:
            _pr.append((_, prop))

    return sorted([(_.area, _id, labels == (_id + 1), _) for (_id, _) in _pr], reverse=True)


def idea1(img_path: Path):
    plt.switch_backend("tkagg")
    print(img_path)

    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # _, binary = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
    _pshow(binary)
    masks = get_largest_component(binary)
    if masks:
        _, _, _m, prop = masks[0]
        for _, _, m, _ in masks[1:]:
            _m |= m
        print(len(masks))
        _pshow(_m)


def idea2(img_path: Path):
    print(img_path)
    # plt.switch_backend("tkagg")

    _img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    __img = cv2.cvtColor(_img, cv2.COLOR_GRAY2RGB)

    sobel = filters.sobel(_img)
    _pshow(sobel)
    blurred = filters.gaussian(sobel, sigma=1.0)
    # blurred = filters.gaussian(sobel, sigma=2.0)
    _pshow(blurred)
    _, tblurred = cv2.threshold(np.round(blurred * 255.0).astype(np.uint8), 20, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(tblurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _show(cv2.drawContours(__img.copy(), cnts, -1, (255, 0, 0), 20))


if __name__ == "__main__":
    img_paths = parse_args()
    *_, = map(idea2, filter_by_ext(img_paths))
