# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx

from lib.genres import genre_overlaps, genres_and_members


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
        fig, ax = plt.subplots(figsize=(16, 9))

        nx.draw_kamada_kawai(
            graph,
            with_labels=True,
            ax=ax,
            nodelist=node_list,
            node_size=size_list,
            node_color="#0e1b3a",
            edge_color="#6177aa",
            font_color="#b9cdfb",
            style="dotted",
        )

        fig.set_facecolor("#2e4272")

    return graph


if __name__ == "__main__":
    from lib.user import User

    user = User()

    artists = user.artists()

    genre_map(artists, size_min=14, draw=True)
