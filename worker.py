from pathlib import Path
import functools
import operator

from constants import Metakey
from common import foreach_leaf, target_path

def files(data, prefix=Path('.')):
    target = prefix / data.metadata[Metakey.target]
    if not data.subnodes:
        yield target
    for s in data.subnodes:
        for f in files(s, target):
            yield f

def missing_files(data, prefix=Path('.')):
    return (
        f for f in files(data, prefix)
        if not f.exists()
    )

def tag_missing(data):
    def _set_tag(*path):
        path[-1].metadata[Metakey.missing] = not functools.reduce(
            operator.truediv,
            (
                p.metadata[Metakey.target]
                for p in path
            ),
            Path('.')
        ).exists()

    foreach_leaf(data, _set_tag)

    return data

def print_matched(data):
    def _print(*path):
        if Metakey.matched not in path[-1].metadata: return
        print(f'{path[-1].metadata[Metakey.matched]} -> {target_path(*path).as_posix()}') 
    foreach_leaf(data, _print)
