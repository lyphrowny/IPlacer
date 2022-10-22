from itertools import chain
from pathlib import Path
from typing import Iterable


def iterdir(path: Path, *, recursive=True):
    if path.is_file():
        yield path
    else:
        yield from recursive and chain.from_iterable(map(iterdir, path.iterdir())) or path.iterdir()


def filter_by_ext(paths: Iterable[Path], exts: Iterable[str] = None):
    if exts is None:
        exts = {".jpg", ".jpeg"}
    exts = map(lambda e: f"{'.' * (e[:1] != '.')}{e}", exts)
    return filter(lambda p: p.suffix in exts, paths)
