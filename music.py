from constants import Metakey
from pathlib import Path
import functools

from common import foreach_matched, quote, escape, target_path

import operator
import math
import os

Metakey.year = 'year'

def convert_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    os.system(' '.join([
        'ffmpeg',
        '-i', quote(escape(source.as_posix())),
        quote(escape(target.as_posix()))
    ]))

def set_metadata(data, artist, album, track):
    os.system(' '.join([
        'mid3v2',
        '-a', quote(escape(artist.metadata[Metakey.name])),
        '-A', quote(escape(album.metadata[Metakey.name])),
        '-t', quote(escape(track.metadata[Metakey.name])),
        '-y', quote(album.metadata[Metakey.year]),
        '-T', quote(f'{track.metadata[Metakey.index] + 1}/{len(album.subnodes)}'),
        quote(escape(target_path(data, artist, album, track).as_posix()))
    ]))

def set_metadata_on_matched(data):
    foreach_matched(data, set_metadata)

def convert_matched(data):
    def _convert(*path):
        convert_file(path[-1].metadata[Metakey.matched], target_path(*path))

    foreach_matched(data, _convert)

def set_targets(root, library, extension):
    library.metadata[Metakey.target] = Path(root)
    for artist in library.subnodes:
        artist.metadata[Metakey.target] = _artist_path(artist)
        for album in artist.subnodes:
            album.metadata[Metakey.target] = _album_path(album)
            for track in album.subnodes:
                track.metadata[Metakey.target] = _track_path(track, extension, len(album.subnodes))

def _artist_path(artist):
    return Path(f'{artist.metadata[Metakey.name]}')

def _album_path(album):
    return Path(f'{album.metadata[Metakey.year]} - {album.metadata[Metakey.name]}')

def _track_path(track, extension, max_track):
    return Path(f'{(track.metadata[Metakey.index]+1):0{math.ceil(math.log10(max_track))}d} {track.metadata[Metakey.name]}.{extension}')
