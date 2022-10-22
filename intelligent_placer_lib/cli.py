from functools import partial
from pathlib import Path
import argparse
from itertools import chain
from utils import iterdir

_IMG_PATH = "img_path"
_RECURSIVE = "-r"


def _build_cli():
    desc = "Determine by the passed image, whether all the objects from the image can be placed inside the polygon, " \
           "depicted on the same photo, without mutual intersection.\n\n" \
           "Returns the set of the objects placed inside the polygon."
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=desc)
    parser.add_argument(_RECURSIVE, action="store_true",
                        help="if specified, the recursive search on every passed dir will be performed "
                             "(default: %(default)s)")
    parser.add_argument(_IMG_PATH, nargs="+", type=Path,
                        help="input file, input files, input dir, input dirs or mix of files and dirs")
    return parser


def parse_args():
    parsed = vars(_build_cli().parse_args())
    return chain.from_iterable(map(partial(iterdir, recursive=parsed[_RECURSIVE[1:]]), parsed[_IMG_PATH]))
