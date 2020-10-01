# -*- coding: utf-8 -*-
from itertools import combinations
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
from artist import Artist


def expand(artists, graph=None):
    """
    Gets each artists' related artists and adds to graph.

    Creates new graph from artists if not supplied.
    Copies graph if supplied; does not modify in place.
    (a, r) edge will be added for every artist a and related artist r.
    """
    artists = {Artist(artist) for artist in artists}

    if graph is None:
        graph = nx.Graph()
    else:
        graph = graph.copy()

    graph.add_nodes_from(artists)

    for artist in artists:
        graph.add_edges_from((artist, related)
                             for related in artist.related())

    return graph


def grow(seeds, graph=None):
    """
    Expands the graph until the seed artists are connected.

    Creates new graph from artists if not supplied.
    Copies graph if supplied; does not modify in place.
    """
    seeds = {Artist(seed) for seed in seeds}

    if graph is None:
        graph = nx.Graph()
    else:
        graph = graph.copy()

    graph.add_nodes_from(seeds)

    new_artists = seeds

    while not all(nx.has_path(graph, source, target)
                  for source, target in combinations(seeds, 2)):
        new_graph = expand(new_artists, graph)
        new_artists = new_graph.nodes - graph.nodes
        graph = new_graph
        if not new_artists:
            raise RuntimeError("No new artists found.")

    for artist in new_artists:
        for related in artist.related():
            if related in graph.nodes:
                graph.add_edge(artist, related)  # new interconnections

    return graph


def trim(graph, keepers=()):
    """
    Iteratively removes leaves from graph.

    Does not modify graph in place.
    """
    graph = graph.copy()

    # Remove leaves until none left.
    while True:
        to_remove = [x for x in graph.nodes
                     if graph.degree(x) < 2 and x not in keepers]
        if to_remove:
            graph.remove_nodes_from(to_remove)
        else:
            break

    return graph


def paths_subgraph(seeds, graph, max_len=None):
    """
    Returns the subgraph of graph containing paths between seeds.

    If max_len is None, only the shortest paths between each pair of seeds will
    be included. Otherwise, only the paths with length <= max_len will be
    included.
    """
    graph = graph.copy()

    paths = []

    for pair in combinations(seeds, 2):
        pair_max_len = max_len  # Specifically for when max_len is None.
        for path in nx.shortest_simple_paths(graph, *pair):
            if pair_max_len is None:
                paths.append(path)
                # Set pair_max_len to shortest length between paired nodes.
                pair_max_len = len(paths[-1])
            elif len(path) <= pair_max_len:
                paths.append(path)
            else:  # nx.shortest_simple_paths yields paths of increasing length
                break

    keepers = set()

    for path in paths:
        keepers.update(path)

    graph.remove_nodes_from(graph.nodes - keepers)

    return graph


def plot(graph,
         seeds=(),  # for coloring purposes
         near_color="#6177aa",
         far_color="#0e1b3a",
         edge_color="#000102",
         font_color="#b9cdfb",
         fig_color="#2e4272",
         save=False,
         **plot_kwargs  # passed to nx.draw
         ):
    seeds = {Artist(seed) for seed in seeds}

    if seeds - graph.nodes:
        raise ValueError("Not all seeds are in graph.")

    dist = {seed: 0 for seed in seeds}

    if seeds and all(nx.has_path(graph, source, target)
                     for source, target in combinations(seeds, 2)):  # XXX
        pres = []
        dists = []

        for i, artist_id in enumerate(seeds):
            pres.append(nx.bfs_predecessors(graph, artist_id))
            dists.append({artist_id: 0})

        for i, artist_id in enumerate(seeds):
            for artist, pre in pres[i]:
                dists[i][artist] = dists[i][pre] + 1

        for artist_id in graph.nodes:
            dist[artist_id] = min(map(lambda d: d.get(artist_id, 1),
                                      dists))

    for artist_id in graph.nodes:
        if artist_id not in dist:
            dist[artist_id] = 1

    max_dist = max(max(dist.values()), 1)

    color = {k: dist[k] / max_dist for k in graph.nodes}

    node_labels = {artist_id:
                   Artist(artist_id).name.replace(r"$", r"\$")
                   for artist_id in graph.nodes}

    cmap = LinearSegmentedColormap.from_list("music",
                                             [near_color,
                                              far_color])

    fig, ax = plt.subplots(figsize=(16, 9))

    nx.draw_kamada_kawai(graph,
                         with_labels=True,
                         ax=ax,
                         cmap=cmap,
                         node_color=[color[k] for k in graph.nodes],
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
                    "-".join(a.id for a in sorted(seeds)) +
                    ".png",
                    facecolor=fig_color)

    return fig, ax


def grow_and_plot(*seeds, graph=None, **plot_kw):
    seeds = {Artist(seed) for seed in seeds}

    graph = grow(seeds, graph=graph)
    graph = trim(graph, keepers=seeds)
    graph = paths_subgraph(seeds, graph)

    return graph, plot(graph, seeds=seeds, **plot_kw)


if __name__ == "__main__":
    from artist_ids import ids

    grow_and_plot(ids["alice coltrane"], ids["erykah badu"])

    grow_and_plot(ids["alice coltrane"], ids["erykah badu"], ids["sun ra"])
