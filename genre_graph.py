# -*- coding: utf-8 -*-
import networkx as nx

from music_tools.genres import genre_overlaps, genres_and_members


def genre_map(artists, *, size_min=1, draw=False):
    """Creates a graph of genres connected by shared artists."""
    graph = nx.Graph()
    graph.add_edges_from(genre_overlaps(artists))

    genre_artists = genres_and_members(artists)

    sizes = {g: len(g_artists) for g, g_artists in genre_artists.items()}

    graph.remove_nodes_from(g for g, size in sizes.items() if size < size_min)

    node_list = list(graph)

    size_list = [20 + 40 * sizes[g] for g in node_list]  # XXX

    if draw:
        nx.draw_kamada_kawai(
            graph,
            with_labels=True,
            nodelist=node_list,
            node_size=size_list,
            edge_color="gray",
            style="dotted",
        )

    return graph


if __name__ == "__main__":
    from music_tools.user import User

    user = User(input("username: "))

    artists = user.artists()

    genre_map(artists, size_min=14, draw=True)
