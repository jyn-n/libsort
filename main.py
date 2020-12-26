#! /usr/bin/env python

import pathlib
import sys
import argparse

import matcher
import music
import worker
import load

argparser = argparse.ArgumentParser()
argparser.add_argument('-s', '--source', required=True, help='source directory')
argparser.add_argument('-t', '--target', required=True, help='target directory')
argparser.add_argument('-i', '--input', required=True, help='input file')
argparser.add_argument('-e', '--extension', default='opus', help='target extension')
argparser.add_argument('-l', '--list-match', action='store_true', help='match files in directory in alphabetical order')
argparser.add_argument('-D', '--dry-run', action='store_true', help='only print what would be done')

options = argparser.parse_args(sys.argv[1:])

source = pathlib.Path(options.source)
target = pathlib.Path(options.target)
input_file = pathlib.Path(options.input)


data = load.read_file(input_file)
music.set_targets(target, data, 'opus')

worker.tag_missing(data)

if options.list_match:
    m = matcher.ListMatcher(source)
else:
    m = matcher.UnsortedMatcher(source)

m.set_matched(data)

if options.dry_run:
    worker.print_matched(data)
    exit(0)

music.convert_matched(data)

