# -*- coding: utf-8 -*-
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artists import get_artist_name


def plot(finder,
         node_color_near="#6177aa",
         node_color_far="#0e1b3a",
         edge_color="#000102",
         font_color="#b9cdfb",
         fig_color="#2e4272",
         save=False,
         **plot_kwargs  # passed to nx.draw
         ):

    if not finder.is_grown:
        raise RuntimeError("finder.grow() must be called before plot()")

    dist = {artist_id: 0 for artist_id in finder.artists}

    if finder.paths:
        pres = []
        dists = []

        for i, artist_id in enumerate(finder.artists):
            pres.append(nx.bfs_predecessors(finder.G_cut, artist_id))
            dists.append({artist_id: 0})

        for i, artist_id in enumerate(finder.artists):
            for artist, pre in pres[i]:
                dists[i][artist] = dists[i][pre] + 1

        for artist_id in finder.G_cut.nodes:
            dist[artist_id] = min(map(lambda d: d.get(artist_id, 1),
                                      dists))

    for artist_id in finder.G_cut.nodes:
        if artist_id not in dist:
            dist[artist_id] = 1

    max_dist = max(max(dist.values()), 1)

    color = {k: dist[k] / max_dist for k in finder.G_cut.nodes}

    node_labels = {artist_id:
                   get_artist_name(artist_id).replace(r"$", r"\$")
                   for artist_id in finder.G_cut.nodes}

    cmap = LinearSegmentedColormap.from_list("music",
                                             [node_color_near,
                                              node_color_far])

    fig, ax = plt.subplots(figsize=(16, 9))

    nx.draw_kamada_kawai(finder.G_cut,
                         with_labels=True,
                         ax=ax,
                         cmap=cmap,
                         node_color=[color[k] for k in finder.G_cut.nodes],
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
                    "-".join(a.id for a in finder.artists) +
                    ".png",
                    facecolor=fig_color)

    return fig, ax


def grow_and_plot(finder, **plot_kw):
    finder.grow()
    finder.trim()
    return plot(finder, **plot_kw)


if __name__ == "__main__":
    from artist_finder import Finder
    from artist_ids import ids

    seeds = [ids[a] for a in ("alice coltrane", "swans")]

    finder = Finder(*seeds)

    fig, ax = grow_and_plot(finder, save=True)
