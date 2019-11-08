# -*- coding: utf-8 -*-
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artist_finder import Finder
from utils import get_artist, get_artist_name, plt_safe


class ArtistGraph(object):
    def __init__(self, *artist_ids):
        self.artists = sorted(get_artist(k) for k in artist_ids)

        self.finder = Finder(*self.artists)

    @property  # XXX
    def G_cut(self):
        return self.finder.G_cut

    def plot(self,
             node_color_near="#6177aa",
             node_color_far="#0e1b3a",
             edge_color="#000102",
             font_color="#b9cdfb",
             fig_color="#2e4272",
             save=False,
             **plot_kwargs  # passed to nx.draw
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
        self.finder.grow()
        self.finder.trim()
        return self.plot(**plot_kw)


if __name__ == "__main__":
    from artist_ids import ids

#    artists = [ids[a] for a in ("death grips",
#                                "earl sweatshirt",
#                                "king krule")]

#    artists = [ids[a] for a in ("akron family",
#                                "sturgill simpson",
#                                "thom yorke")]

    artists = [ids[a] for a in ("black sabbath",
                                "magazine")]

    artist_graph = ArtistGraph(*artists)

    fig, ax = artist_graph.grow_and_plot(save=True)
