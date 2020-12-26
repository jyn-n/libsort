from pathlib import Path

from constants import Metakey
import functools
import operator


def leaves(data):
    for l in leaves_with_paths(data):
        yield l[-1]

def leaves_with_paths(data, *prefix):
    if not data.subnodes:
        yield (data,)

    for s in data.subnodes:
        for l in leaves_with_paths(s):
            yield data, *l

def foreach_leaf(data, action):
    for l in leaves_with_paths(data):
        action(*l)

def target_path(*path):
    return functools.reduce(
        operator.truediv,
        (p.metadata[Metakey.target] for p in path),
        Path('.')
    )

def escape(string):
    return str(string).replace("'", "'\"'\"'")

def quote(string):
    return '"' + str(string) + '"'

