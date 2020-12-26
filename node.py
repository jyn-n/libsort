class Node:
    def __init__(self, metadata=dict(), subnodes=list()):
        self._metadata = metadata
        self._subnodes = subnodes

    @property
    def metadata(self):
        return self._metadata

    @property
    def subnodes(self):
        return self._subnodes

    def __repr__(self):
        r = f'{self.metadata}'
        if self._subnodes:
            r += f', {self.subnodes}'

        return r
