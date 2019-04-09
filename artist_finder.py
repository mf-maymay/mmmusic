# -*- coding: utf-8 -*-
from functools import reduce
from utils import get_artist_name, get_related


class Finder(object):
    def __init__(self, *artist_ids):
        self.artist_ids = artist_ids

        self.artist_names = {k: get_artist_name(k) for k in self.artist_ids}

        self.sets = {k: {k} for k in self.artist_ids}

        self.edges = set()

        self.lasts = {k: s.copy() for k, s in self.sets.items()}

    def expand(self):
        for k in self.artist_ids:
            new = set()
            for artist in self.lasts[k]:
                add = {related["id"] for related in get_related(artist)}
                self.edges |= {(artist, related) for related in add}
                new |= add
            self.lasts[k] = new - self.sets[k]
            self.sets[k] |= self.lasts[k]

    def find(self):
        # TODO: Consider changing condition for greater numbers of artists.
        while not self.midpoints(names=False):
            self.expand()

    def midpoints(self, names=True):
        if names:
            return sorted(map(get_artist_name, self.midpoints(names=False)))
        else:
            return reduce(set.intersection, self.sets.values())


if __name__ == "__main__":
    from artist_ids import ids

    finder = Finder(ids["death grips"], ids["earl sweatshirt"])
