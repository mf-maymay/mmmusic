# -*- coding: utf-8 -*-
from functools import reduce
from itertools import combinations
import networkx as nx
from utils import get_artist, get_related


class Finder(object):
    def __init__(self, *artist_ids):
        self.artists = {get_artist(k) for k in artist_ids}

        self.sets = {artist: {artist} for artist in self.artists}

        self.farthest = {artist: {artist} for artist in self.artists}

        self.G = nx.Graph()
        self.G.add_nodes_from(self.artists)

        self.is_grown = False

        self._G_cut = None  # subset of G

        self.paths = None

        self.max_path_len = None

    @property  # XXX
    def G_cut(self):
        if self._G_cut is None:
            self._G_cut = self.G.copy()
        return self._G_cut

    def expand(self):
        for artist in self.artists:
            new = set()
            for fartist in self.farthest[artist]:
                related = {get_artist(rel) for rel in get_related(fartist)}
                self.G.add_edges_from({(fartist, rel) for rel in related})
                new |= related
            self.farthest[artist] = new - self.sets[artist]
            self.sets[artist] |= self.farthest[artist]

    def midpoints(self):
        return reduce(set.intersection, self.sets.values())

    def grow(self):
        if self.is_grown:
            self.expand()
        else:
            while not nx.is_connected(self.G):
                self.expand()

        for artist in self.midpoints():
            for related in get_related(artist):
                if related in self.G.nodes:
                    self.G.add_edge(artist, related)

        self.is_grown = True

    def trim(self):
        self._G_cut = None

        print("Nodes (initial):", len(self.G_cut.nodes))

        # first trim - remove leaves until none left
        while True:
            to_remove = []
            for node in self.G_cut.nodes:
                if self.G_cut.degree(node) < 2:
                    if node not in self.artists:
                        to_remove.append(node)
            if to_remove:
                self.G_cut.remove_nodes_from(to_remove)
            else:
                break

        print("Nodes (post-first-trim):", len(self.G_cut.nodes))

        # second trim - only keep nodes belonging to desired paths
        self.paths = []

        if self.max_path_len is not None:
            self.max_path_len += 1

        # XXX: below needs updating for multiple roots, due to max_path_len
        for start, stop in combinations(self.artists, 2):
            try:
                for path in nx.shortest_simple_paths(self.G_cut, start, stop):
                    if ((not self.paths) or
                        ((len(path) == len(self.paths[-1])) if
                         (self.max_path_len is None) else
                         (len(path) <= self.max_path_len))):
                        self.paths.append(path)
                    else:
                        break
            except nx.NetworkXNoPath as e:
                print(e.args[0])
                continue

        keepers = set(self.artists)

        if self.paths:
            self.max_path_len = max(map(len, self.paths))

            keepers |= reduce(set.union, map(set, self.paths))

        self.G_cut.remove_nodes_from(set(self.G_cut.nodes) - keepers)

        print("Nodes (post-paths-trim):", len(self.G_cut.nodes))


if __name__ == "__main__":
    from artist_ids import ids

    finder = Finder(ids["death grips"], ids["earl sweatshirt"])

    finder.grow()

    for midpoint in sorted(finder.midpoints()):
        print(midpoint)
