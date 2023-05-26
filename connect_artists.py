import argparse
from itertools import combinations
from pathlib import Path
from typing import Any
import webbrowser

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx

from lib.models.artists import get_artist, get_artist_related_artists, search_for_artist


def expand(artists, graph=None) -> nx.Graph:
    """
    Adds each artists' related artists to graph.

    Args:
        artists: An iterable of Artist objects or strings of artist IDs.
        graph: Optional; A networkx.Graph instance. graph is copied and not
            modified in-place. If graph is None, an empty graph is used.

    Returns:
        A networkx.Graph instance with Artist objects as nodes, with the graph
        argument as a subgraph, and with an edge (a, r) for each artist, a,
        from the artists argument and each related artist of a, r.
    """
    artists = {get_artist(artist) for artist in artists}

    graph = nx.Graph() if graph is None else graph.copy()
    graph.add_nodes_from(artists)

    for artist in artists:
        graph.add_edges_from(
            (artist, related) for related in get_artist_related_artists(artist)
        )
    return graph


def grow(seeds, graph=None) -> nx.Graph:
    """
    Expands graph until the seed artists are connected by related artists.

    Args:
        seeds: An iterable of Artist objects or strings of artist IDs.
        graph: Optional; A networkx.Graph instance. graph is copied and not
            modified in-place. If graph is None, an empty graph is used.

    Returns:
        A networkx.Graph instance with Artist objects as nodes, with the graph
        argument as a subgraph, and with each object in the seeds argument
        within and connected to each other by paths of related artists.
    """
    seeds = {get_artist(seed) for seed in seeds}

    graph = nx.Graph() if graph is None else graph.copy()
    graph.add_nodes_from(seeds)

    new_artists = seeds

    while not all(
        nx.has_path(graph, source, target) for source, target in combinations(seeds, 2)
    ):
        new_graph = expand(new_artists, graph)
        new_artists = new_graph.nodes - graph.nodes
        graph = new_graph
        if not new_artists:
            raise RuntimeError("No new artists found.")
    for artist in new_artists:
        for related in get_artist_related_artists(artist):
            if related in graph.nodes:
                graph.add_edge(artist, related)  # new interconnections
    return graph


def trim(graph, keepers=()) -> nx.Graph:
    """
    Iteratively removes leaves from graph.

    Args:
        graph: A networkx.Graph instance. graph is copied and not modified
            in-place.
        keepers: Optional; A container of items to be kept in graph.

    Returns:
        A networkx.Graph instance. A subgraph of the graph argument without any
        leaves, except for nodes specified by the keepers argument (if any).
    """
    graph = graph.copy()

    while to_remove := [
        node for node in graph.nodes if graph.degree(node) < 2 and node not in keepers
    ]:
        graph.remove_nodes_from(to_remove)

    return graph


def paths_subgraph(graph, seeds, max_len=None) -> tuple[nx.Graph, dict]:
    """
    Returns the subgraph of graph containing only the paths between seeds.

    Args:
        graph: A networkx.Graph instance. graph is copied and not modified
            in-place.
        seeds: An iterable containing nodes in the graph argument.
        max_len: Optional; If max_len is None, only the shortest paths between
            each pair of seeds will be included. Otherwise, only the paths with
            length <= max_len will be included.

    Returns:
        A tuple (G, paths_dict) containing a networkx.Graph instance (G) and
        a dictionary (paths_dict).

        G is a subgraph of the graph argument wherein each node belongs to one
        of the shortest simple paths between the nodes specified by the seeds
        argument.

        paths_dict maps pairs of seeds (as tuples) to the paths between them
        (as lists of lists).
    """
    graph = graph.copy()

    paths_per_pair: dict[tuple[Any, Any], list] = {}

    for pair in combinations(seeds, 2):
        paths_per_pair[pair] = []
        pair_max_len = max_len  # Specifically for when max_len is None.
        for path in nx.shortest_simple_paths(graph, *pair):
            if pair_max_len is None:
                paths_per_pair[pair].append(path)
                # Set pair_max_len to shortest length between paired nodes.
                pair_max_len = len(paths_per_pair[pair][-1])
            elif len(path) <= pair_max_len:
                paths_per_pair[pair].append(path)
            else:  # nx.shortest_simple_paths yields paths of increasing length
                break
    keepers = set()

    for paths in paths_per_pair.values():
        for path in paths:
            keepers.update(path)

    graph.remove_nodes_from(graph.nodes - keepers)

    return graph, paths_per_pair


def plot(
    graph,
    seeds=(),  # for coloring purposes
    near_color="#6177aa",
    far_color="#0e1b3a",
    edge_color="#000102",
    font_color="#b9cdfb",
    fig_color="#2e4272",
    **plot_kwargs,  # passed to nx.draw
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plots the graph.

    The graph is plotted using networkx.draw_kamada_kawai. If the seeds
    argument is supplied, the nodes will vary in color based on proximity to
    the nodes in seeds, from near_color to far_color.

    Args:
        graph: A networkx.Graph instance.
        seeds: Optional; A container of items in graph. If supplied, the nodes,
            when plotted, will be colored based on proximity to the nodes in
            seeds.
        near_color: Optional; A string representing a color for matplotlib.
            The nodes in seeds will be this color. If the seeds argument is not
            supplied, all nodes will be this color.
        far_color: Optional; A string representing a color for matplotlib.
            The nodes farthest away from the nodes in seeds will be this color.
            If the seeds argument is not supplied, then no nodes will be this
            color.
        edge_color: Optional; A string representing a color for matplotlib.
        font_color: Optional; A string representing a color for matplotlib.
        fig_color: Optional; A string representing a color for matplotlib.
        plot_kwargs: Optional; Keyword arguments to pass to networkx.draw (and
            to matplotlib, by extention).

    Returns:
        A tuple (fig, ax) containing the created plt.Figure (fig) and plt.Axes
        (ax) objects.
    """
    seeds = {get_artist(seed) for seed in seeds}

    if seeds - graph.nodes:
        raise ValueError("Not all seeds are in graph.")
    dist = {seed: 0 for seed in seeds}

    if seeds and all(
        nx.has_path(graph, source, target) for source, target in combinations(seeds, 2)
    ):  # XXX
        pres = []
        dists = []

        for artist_id in seeds:
            pres.append(nx.bfs_predecessors(graph, artist_id))
            dists.append({artist_id: 0})
        for i, artist_id in enumerate(seeds):
            for artist, pre in pres[i]:
                dists[i][artist] = dists[i][pre] + 1
        for artist_id in graph.nodes:
            dist[artist_id] = min(map(lambda d: d.get(artist_id, 1), dists))
    for artist_id in graph.nodes:
        if artist_id not in dist:
            dist[artist_id] = 1
    max_dist = max(max(dist.values()), 1)

    color = {k: dist[k] / max_dist for k in graph.nodes}

    node_labels = {
        artist_id: get_artist(artist_id).name.replace(r"$", r"\$")
        for artist_id in graph.nodes
    }

    cmap = LinearSegmentedColormap.from_list("music", [near_color, far_color])

    fig, ax = plt.subplots(figsize=(16, 9))

    nx.draw_kamada_kawai(
        graph,
        with_labels=True,
        ax=ax,
        cmap=cmap,
        node_color=[color[k] for k in graph.nodes],
        edge_color=edge_color,
        font_color=font_color,
        labels=node_labels,
        **plot_kwargs,
    )

    fig.set_facecolor(fig_color)

    fig.tight_layout()

    return fig, ax


def grow_and_plot(
    *seeds, graph=None, **plot_kw
) -> tuple[nx.Graph, tuple[plt.Figure, plt.Axes]]:
    """
    Grows and plots the graph grown from seeds.

    Grows the graph, trims it, gets the subgraph of its paths, and plots it.

    Args:
        seeds: Artist objects or strings of artist IDs
        graph: Optional; A networkx.Graph instance. graph is copied and not
            modified in-place. If graph is None, an empty graph is used.
        plot_kw: Optional; Keyword arguments to pass to networkx.draw (and
            to matplotlib, by extention).

    Returns:
        A tuple (G, (fig, ax)) containing a networkx.Graph instance (g) -- with
        Artist objects as nodes, and wherein each node belongs to one of the
        shortest simple paths of related artists between the nodes specified by
        the seeds argument -- and the created plt.Figure (fig) and plt.Axes
        (ax) objects.
    """
    seed_artists = {get_artist(seed) for seed in seeds}

    graph = grow(seed_artists, graph=graph)
    graph = trim(graph, keepers=seed_artists)
    graph, _ = paths_subgraph(graph, seed_artists)

    return graph, plot(graph, seeds=seed_artists, **plot_kw)


if __name__ == "__main__":
    # example usage:
    # python connect_artists.py 0oKYiTD5CdNbrofRvM1dIr 0tIODqvzGUoEaK26rK4pvX

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "artists", nargs="*", help=("artists (as IDs or names), separated by spaces")
    )
    args = parser.parse_args()

    inputs = args.artists or [input("Artist #1: "), input("Artist #2: ")]

    seeds = [search_for_artist(artist) for artist in inputs]

    print("Connecting {} ...".format(" and ".join(f"'{seed}'" for seed in seeds)))

    graph, (fig, ax) = grow_and_plot(*seeds)

    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    file_path = output_folder / f'{"-".join(sorted(seed.id for seed in seeds))}.png'
    fig.savefig(file_path)

    webbrowser.open(str(file_path))
