# -*- coding: utf-8 -*-
from collections import namedtuple

_Album = namedtuple("_Album", ("id", "name", "artist_ids"))


class Album(_Album):
    __slots__ = ()

    def __eq__(self, other):
        return (hash(self) == hash(other))

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return (self.name < str(other))

    def __str__(self):
        return self.name
