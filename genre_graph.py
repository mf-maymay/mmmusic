# -*- coding: utf-8 -*-
import networkx as nx
from networkx.algorithms.approximation import clique_removal
from genres import genre_overlaps, genres_and_members


def genre_map(size_min, artists, draw=False):
    """Creates a graph of genres connected by shared artists."""
    graph = nx.Graph()
    graph.add_edges_from(genre_overlaps(artists))

    genre_artists = genres_and_members(artists)

    graph.remove_nodes_from(g for g in genre_artists
                            if len(genre_artists[g]) <= size_min)

    if draw:
        nx.draw_kamada_kawai(graph, with_labels=True, edge_color="gray",
                             style="dotted")

    return graph


def cliques(artists=None, graph=None):
    if graph is None:
        if artists is None:
            raise ValueError("artists and graph cannot both be None")
        else:
            graph = genre_map(0, artists)

    if artists is None:
        artists = set(graph.nodes)

    largest_independent_set, maximal_cliques = clique_removal(
        genre_map(0, artists)
    )

    genre_artists = genres_and_members(artists)

    groups = {}

    for clique in maximal_cliques:
        clique = sorted(clique, key=lambda c: (-len(genre_artists[c]), c))
        groups[clique[0].upper()] = clique

    groups_list = sorted(
        groups.items(),
        key=lambda c: (-sum(len(genre_artists[g]) for g in c[1]), c[0])
    )

    return groups_list  # XXX


if __name__ == "__main__":
    from user import User

    user = User(input("username: "))

    artists = user.artists()

    genre_map(20, artists, draw=True)

    groups_list = cliques(artists=artists)

    genre_artists = genres_and_members(artists)

    for rep, clique in groups_list:
        clique_sizes = [len(genre_artists[genre]) for genre in clique]
        print(f"{rep} ({sum(clique_sizes)}):")
        for genre, size in zip(clique, clique_sizes):
            print(f"\t{genre} ({size})")
