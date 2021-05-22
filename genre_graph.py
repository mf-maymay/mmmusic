# -*- coding: utf-8 -*-
import networkx as nx
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


if __name__ == "__main__":
    from networkx.algorithms.approximation import clique_removal
    from user import User

    user = User(input("username: "))

    artists = user.artists()

    graph = genre_map(20, artists, draw=True)

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

    print("\n".join(f"{rep}:\n\t" +
                    "\n\t".join(f"{c} ({len(genre_artists[c])})"
                                for c in clique)
                    for rep, clique in groups_list))
