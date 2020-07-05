# -*- coding: utf-8 -*-
from functools import reduce
from itertools import combinations
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artists import get_artist, get_artist_name, get_related


class Finder(object):
    def __init__(self, *artist_ids):
        self.artists = {get_artist(k) for k in artist_ids}

        self.sets = {artist: {artist} for artist in self.artists}

        self.farthest = {artist: {artist} for artist in self.artists}

        self.G = nx.Graph()  # undirected
        self.G.add_nodes_from(self.artists)

        self.is_grown = False

        self.G_cut = None  # subset of G

        self.paths = None

        self.max_path_len = None

    def expand(self):
        """
        Expands each initial artist's network.

        Gathers the related artists of newest members of initial artists' sets.
        """
        for artist in self.artists:
            new = set()
            for farthest in self.farthest[artist]:
                related = {get_artist(rel) for rel in get_related(farthest)}
                self.G.add_edges_from({(farthest, rel) for rel in related})
                new |= related
            self.farthest[artist] = new - self.sets[artist]
            self.sets[artist] |= self.farthest[artist]

    def midpoints(self):
        """Returns the artists that belong to all initial artists' sets."""
        return reduce(set.intersection, self.sets.values())

    def grow(self):
        """
        Expands the graph until the initial artists are connected.

        If the graph is already connected, it is expanded once.
        """
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
        self.G_cut = self.G.copy()

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

        combo_path_gens = [nx.shortest_simple_paths(self.G_cut, start, stop)
                           for start, stop in combinations(self.artists, 2)]

        paths_to_add = True

        while paths_to_add:
            paths_to_add = False
            for path_gen in combo_path_gens:
                path = next(path_gen, None)
                if path is not None:
                    if ((not self.paths) or
                        (self.max_path_len is not None and
                         len(path) <= self.max_path_len)):
                        self.paths.append(path)
                        paths_to_add = True
            if self.paths and self.max_path_len is None:
                self.max_path_len = max(map(len, self.paths))

        keepers = set(self.artists)

        if self.paths:
            keepers |= reduce(set.union, map(set, self.paths))

        self.G_cut.remove_nodes_from(set(self.G_cut.nodes) - keepers)

        print("Nodes (post-paths-trim):", len(self.G_cut.nodes))

    def plot(self,
             node_color_near="#6177aa",
             node_color_far="#0e1b3a",
             edge_color="#000102",
             font_color="#b9cdfb",
             fig_color="#2e4272",
             save=False,
             **plot_kwargs  # passed to nx.draw
             ):

        if not self.is_grown:
            raise RuntimeError("grow() must be called before plot()")

        dist = {artist_id: 0 for artist_id in self.artists}

        if self.paths:
            pres = []
            dists = []

            for i, artist_id in enumerate(self.artists):
                pres.append(nx.bfs_predecessors(self.G_cut, artist_id))
                dists.append({artist_id: 0})

            for i, artist_id in enumerate(self.artists):
                for artist, pre in pres[i]:
                    dists[i][artist] = dists[i][pre] + 1

            for artist_id in self.G_cut.nodes:
                dist[artist_id] = min(map(lambda d: d.get(artist_id, 1),
                                          dists))

        for artist_id in self.G_cut.nodes:
            if artist_id not in dist:
                dist[artist_id] = 1

        max_dist = max(max(dist.values()), 1)

        color = {k: dist[k] / max_dist for k in self.G_cut.nodes}

        node_labels = {artist_id:
                       get_artist_name(artist_id).replace(r"$", r"\$")
                       for artist_id in self.G_cut.nodes}

        cmap = LinearSegmentedColormap.from_list("music",
                                                 [node_color_near,
                                                  node_color_far])

        fig, ax = plt.subplots(figsize=(16, 9))

        nx.draw_kamada_kawai(self.G_cut,
                             with_labels=True,
                             ax=ax,
                             cmap=cmap,
                             node_color=[color[k] for k in self.G_cut.nodes],
                             edge_color=edge_color,
                             font_color=font_color,
                             labels=node_labels,
                             **plot_kwargs
                             )

        fig.set_facecolor(fig_color)

        fig.tight_layout()

        if save:
            os.makedirs("output", exist_ok=True)
            fig.savefig("output/" +
                        "-".join(a.id for a in self.artists) +
                        ".png",
                        facecolor=fig_color)

        return fig, ax

    def grow_and_plot(self, **plot_kw):
        self.grow()
        self.trim()
        return self.plot(**plot_kw)


if __name__ == "__main__":
    from artist_ids import ids

    finder = Finder(ids["alice coltrane"], ids["erykah badu"])
    # finder = Finder(ids["alice coltrane"], ids["erykah badu"], ids["sun ra"])
    # XXX: finder for 3 artists not working anymore

    finder.grow_and_plot()

    print()

    for midpoint in sorted(finder.midpoints()):
        print(midpoint)
