# -*- coding: utf-8 -*-
from functools import reduce
from itertools import combinations
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artist_finder import Finder
from utils import get_artist_name, get_related, plt_safe

DEFAULT_NODE_COLOR_NEAR = "#6177aa"
DEFAULT_NODE_COLOR_FAR = "#0e1b3a"
DEFAULT_EDGE_COLOR = "#000102"
DEFAULT_FONT_COLOR = "#b9cdfb"
DEFAULT_FIG_COLOR = "#2e4272"


class ArtistGraph(object):
    def __init__(self, *artist_ids):
        self.artist_ids = artist_ids

        self.finder = Finder(*self.artist_ids)

        self.G = nx.Graph()

        self.G.add_nodes_from(self.artist_ids)

        self.paths = None

        self.max_path_len = None

        self.is_built = False

    def get_artist_names(self):
        return sorted(map(get_artist_name, self.G.nodes))

    def trim(self):
        while True:
            to_remove = []
            for node in self.G.nodes:
                if self.G.degree(node) < 2:
                    if node not in self.artist_ids:
                        to_remove.append(node)
            if to_remove:
                self.G.remove_nodes_from(to_remove)
            else:
                break

    def grow(self, step_only=False):
        if self.is_built or step_only:
            self.finder.expand()
        else:
            self.finder.find()

        self.G.add_edges_from(self.finder.edges)

        for artist in self.finder.midpoints(names=False):
            for related in get_related(artist):
                if related["id"] in self.G.nodes:
                    self.G.add_edge(artist, related["id"])

        print("Nodes (initial):", len(self.G.nodes))

        self.trim()

        print("Nodes (post-first-trim):", len(self.G.nodes))

        self.paths = []

        if self.max_path_len is not None:
            self.max_path_len += 1

        for start, stop in combinations(self.artist_ids, 2):
            try:
                for path in nx.shortest_simple_paths(self.G, start, stop):
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

        keepers = set(self.artist_ids)

        if self.paths:
            self.max_path_len = max(map(len, self.paths))

            keepers |= reduce(set.union, map(set, self.paths))

        self.G.remove_nodes_from(set(self.G.nodes) - keepers)

        print("Nodes (post-paths-trim):", len(self.G.nodes))

        self.is_built = True

    def plot(self,
             node_color_near=DEFAULT_NODE_COLOR_NEAR,
             node_color_far=DEFAULT_NODE_COLOR_FAR,
             edge_color=DEFAULT_EDGE_COLOR,
             font_color=DEFAULT_FONT_COLOR,
             fig_color=DEFAULT_FIG_COLOR,
             save=True,
             only_keep_roots=False
             ):
        if not self.is_built:
            raise RuntimeError("build() must be called before plot()")

        if only_keep_roots:
            self.G.remove_nodes_from(set(self.G.nodes) - set(self.artist_ids))

        dist = {artist_id: 0 for artist_id in self.artist_ids}

        if self.paths:
            pres = []
            dists = []

            for i, artist_id in enumerate(self.artist_ids):
                pres.append(nx.bfs_predecessors(self.G, artist_id))
                dists.append({artist_id: 0})

            for i, artist_id in enumerate(self.artist_ids):
                for artist, pre in pres[i]:
                    dists[i][artist] = dists[i][pre] + 1

            for artist_id in self.G.nodes:
                dist[artist_id] = min(map(lambda d: d.get(artist_id, 1),
                                          dists))

        for artist_id in self.G.nodes:
            if artist_id not in dist:
                dist[artist_id] = 1

        max_dist = max(max(dist.values()), 1)

        color = {k: dist[k] / max_dist for k in self.G.nodes}

        node_labels = {artist_id: plt_safe(get_artist_name(artist_id))
                       for artist_id in self.G.nodes}

        cmap = LinearSegmentedColormap.from_list("music",
                                                 [DEFAULT_NODE_COLOR_NEAR,
                                                  DEFAULT_NODE_COLOR_FAR]
                                                 )

        fig, ax = plt.subplots(figsize=(16, 9))

        nx.draw_kamada_kawai(self.G,
                             with_labels=True,
                             ax=ax,
                             cmap=cmap,
                             node_color=[color[k] for k in self.G.nodes],
                             edge_color=edge_color,
                             font_color=font_color,
                             labels=node_labels
                             )

        fig.set_facecolor(fig_color)

        fig.tight_layout()

        if save:
            fig.savefig("output/" + "-".join(self.artist_ids) + ".png",
                        facecolor=fig_color)

        return fig, ax

    def grow_and_plot(self, step_only=False, **plot_kw):
        self.grow(step_only=step_only)
        return self.plot(**plot_kw)


if __name__ == "__main__":
    from artist_ids import ids

    save = True

    step_only = False

    artists = map(ids.__getitem__, ["picastro", "pretend"])

    artist_graph = ArtistGraph(*artists)

    fig, ax = artist_graph.grow_and_plot(step_only=step_only, save=save)
