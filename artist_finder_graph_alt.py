# -*- coding: utf-8 -*-
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artist_finder_alt import Finder
from utils import get_artist, get_artist_name, plt_safe

DEFAULT_NODE_COLOR_NEAR = "#6177aa"
DEFAULT_NODE_COLOR_FAR = "#0e1b3a"
DEFAULT_EDGE_COLOR = "#000102"
DEFAULT_FONT_COLOR = "#b9cdfb"
DEFAULT_FIG_COLOR = "#2e4272"


class ArtistGraph(object):
    def __init__(self, *artist_ids):
        self.artists = sorted(get_artist(k) for k in artist_ids)

        self.finder = Finder(*self.artists)

    @property  # XXX
    def G_cut(self):
        return self.finder.G_cut

    def plot(self,
             node_color_near=DEFAULT_NODE_COLOR_NEAR,
             node_color_far=DEFAULT_NODE_COLOR_FAR,
             edge_color=DEFAULT_EDGE_COLOR,
             font_color=DEFAULT_FONT_COLOR,
             fig_color=DEFAULT_FIG_COLOR,
             save=True
             ):

        if not self.finder.is_grown:
            raise RuntimeError("finder.grow() must be called before plot()")

        dist = {artist_id: 0 for artist_id in self.artists}

        if self.finder.paths:
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

        node_labels = {artist_id: plt_safe(get_artist_name(artist_id))
                       for artist_id in self.G_cut.nodes}

        cmap = LinearSegmentedColormap.from_list("music",
                                                 [DEFAULT_NODE_COLOR_NEAR,
                                                  DEFAULT_NODE_COLOR_FAR]
                                                 )

        fig, ax = plt.subplots(figsize=(16, 9))

        nx.draw_kamada_kawai(self.G_cut,
                             with_labels=True,
                             ax=ax,
                             cmap=cmap,
                             node_color=[color[k] for k in self.G_cut.nodes],
                             edge_color=edge_color,
                             font_color=font_color,
                             labels=node_labels
                             )

        fig.set_facecolor(fig_color)

        fig.tight_layout()

        if save:  # XXX: use ids, not names ? - ya, some names not good
            fig.savefig("output/" +
                        "-".join(a.id for a in self.artists) +
                        ".png",
                        facecolor=fig_color)  # TODO: make dir if not exists

        return fig, ax

    def grow_and_plot(self, **plot_kw):
        self.finder.grow()
        self.finder.trim()
        return self.plot(**plot_kw)


if __name__ == "__main__":
    from artist_ids import ids

    save = True

#    artists = [ids[a] for a in ("death grips",
#                                "earl sweatshirt",
#                                "king krule")]

    artists = [ids[a] for a in ("akron family",
                                "sturgill simpson",
                                "thom yorke")]

    artist_graph = ArtistGraph(*artists)

    fig, ax = artist_graph.grow_and_plot(save=save)
