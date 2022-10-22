from pathlib import Path
from cli import parse_args
from utils import filter_by_ext


def check_image(img_path: Path):
    ...


if __name__ == "__main__":
    img_paths = parse_args()
    *_, = map(check_image, filter_by_ext(img_paths))
