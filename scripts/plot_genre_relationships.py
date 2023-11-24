import matplotlib.pyplot as plt
import networkx as nx

from mmmusic.genres import genre_overlaps, get_genre_artists_map


def genre_map(artists, *, size_min=1, draw=False):
    """Creates a graph of genres connected by shared artists."""
    graph = nx.Graph()
    graph.add_edges_from(genre_overlaps(artists))

    genre_artists_map = get_genre_artists_map(artists)

    sizes = {genre: len(artists) for genre, artists in genre_artists_map.items()}

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
    from mmmusic.users import User

    user = User()

    artists = user.get_artists_of_saved_albums()

    genre_map(artists, size_min=14, draw=True)
