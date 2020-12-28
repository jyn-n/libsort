#! /usr/bin/env python

import pathlib
import sys
import argparse

import matcher
import music
import worker
import load
import node
from constants import Metakey

def convert(data, options):
    source = pathlib.Path(options.source)

    if options.list_match:
        m = matcher.ListMatcher(source)
    else:
        m = matcher.UnsortedMatcher(source)

    m.set_matched(data)

    if options.dry_run:
        worker.print_matched(data)
        return

    music.convert_matched(data)

    if not options.no_metadata:
        music.set_metadata_on_matched(data)


def list_(data, options):
    def output_line(f, colorized):
        r = f.as_posix()
        if colorized:
            colors = {
                True: '\033[92m',
                False: '\033[91m'
            }
            reset = '\033[0m'
            r = colors[f.exists()] + r + reset

        return r

    for f in worker.files(data):
        if options.missing and f.exists():
            continue
        print(output_line(f, options.color))

argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--target', required=True, help='target directory')
argparser.add_argument('-i', '--input', required=True, help='input file')
argparser.add_argument('-e', '--extension', default='opus', help='target extension')
argparser.add_argument('-R', '--restrict', default='', help='only work on specified subdata')

subparsers = argparser.add_subparsers()

list_parser = subparsers.add_parser('list')
list_parser.set_defaults(func=list_)
list_parser.add_argument('-m', '--missing', action='store_true', help='list missing files only')
list_parser.add_argument('-c', '--color', action='store_true', help='color output by status')

convert_parser = subparsers.add_parser('convert')
convert_parser.set_defaults(func=convert)
convert_parser.add_argument('-s', '--source', required=True, help='source directory')
convert_parser.add_argument('-l', '--list-match', action='store_true', help='match files in directory in alphabetical order')
convert_parser.add_argument('-D', '--dry-run', action='store_true', help='only print what would be done')
convert_parser.add_argument('--no-metadata', action='store_true', help='do not set metadata after converting files')

#mkdir
#specify matches
#set metadata
#move instead of convert

options = argparser.parse_args(sys.argv[1:])

data = load.read_file(pathlib.Path(options.input))
music.set_targets(pathlib.Path(options.target), data, 'opus')

def filter_data(data, filterpath):
    if filterpath == '':
        return data

    def filter(node):
        target = node.metadata[Metakey.target].as_posix()
        return filterpath == target or filterpath.startswith(target+'/')

    def next_path(node):
        target = node.metadata[Metakey.target].as_posix()
        if filterpath == target:
            return ''
        return filterpath[len(target)+1:]

    return node.Node(
        data.metadata,
        [
            filter_data(n, next_path(n))
            for n in data.subnodes
            if filter(n)
        ]
    )

data = filter_data(data, options.restrict)

worker.tag_missing(data)

options.func(data, options)
