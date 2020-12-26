import stringcomparison
from pathlib import Path

from constants import Metakey
from common import leaves

class UnsortedMatcher:
    def __init__(
        self,
        directory,
        file_valid=lambda path: True,
        maximum_relative_distance=1,
        likely_name=lambda needle: needle.metadata[Metakey.name]
    ):
        self._possibilities = [
            path
            for path in Path(directory).iterdir()
            if file_valid(path)
        ]
        self._maximum_relative_distance = maximum_relative_distance
        self._likely_name = likely_name

    def match(self, needle):
        results = stringcomparison.rate(
            self._likely_name(needle),
            self._possibilities,
            distance=lambda needle, path: stringcomparison.relative_distance(needle, path.stem)
        )

        if len(results) == 0:
            return None

        result, distance = results[0]

        return result

    def match_missing(self, data):
        results = {
            needle: self.match(needle)
            for needle in leaves(data)
            if Metakey.missing in needle.metadata and needle.metadata[Metakey.missing]
        }

        return {
            key: value
            for key, value in results.items()
            if value is not None
        }

    def set_matched(self, data):
        for key, value in self.match_missing(data).items():
            key.metadata[Metakey.matched] = value


class ListMatcher:
    def __init__(
        self,
        directory
    ):
        self._directory = directory

    def set_matched(self, data):
        for d, matched in zip(data, Path(self._directory).iterdir()):
            if Metakey.missing in d.metadata and d.metadata[Metakey.missing]:
                d.metadata[Metakey.matched] = matched

