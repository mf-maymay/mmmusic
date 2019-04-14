# -*- coding: utf-8 -*-
from functools import reduce
import networkx as nx
from utils import get_artist, get_related


class Finder(object):
    def __init__(self, *artist_ids):
        self.artists = {get_artist(k) for k in artist_ids}

        self.sets = {artist: {artist} for artist in self.artists}

        self.farthest = {artist: {artist} for artist in self.artists}

        self.G = nx.Graph()

        self.G.add_nodes_from(self.artists)

    def expand(self):
        for artist in self.artists:
            new = set()
            for fartist in self.farthest[artist]:
                related = {get_artist(rel) for rel in get_related(fartist)}
                self.G.add_edges_from({(fartist, rel) for rel in related})
                new |= related
            self.farthest[artist] = new - self.sets[artist]
            self.sets[artist] |= self.farthest[artist]

    def find(self):
        while not nx.is_connected(self.G):
            self.expand()

    def midpoints(self):
        return reduce(set.intersection, self.sets.values())


if __name__ == "__main__":
    from artist_ids import ids

    finder = Finder(ids["death grips"], ids["earl sweatshirt"])

    finder.find()

    for midpoint in sorted(finder.midpoints()):
        print(midpoint)
