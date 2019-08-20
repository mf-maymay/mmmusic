# -*- coding: utf-8 -*-
from collections import Counter, defaultdict
from itertools import permutations
import networkx as nx
import pandas as pd
from artist_info import saved
from utils import get_genres

artist_genres = {}
genre_artists = defaultdict(set)
edges = Counter()


for artist in saved:
    artist_genres[artist] = get_genres(artist)

    for genre in get_genres(artist):
        genre_artists[genre] |= {artist}

    edges.update(permutations(get_genres(artist), 2))


graph = nx.Graph()
graph.add_edges_from(edges.keys())


edf = pd.DataFrame()

cols = list(zip(*((u, v, w) for (u, v), w in edges.items())))

edf["g1"], edf["g2"], edf["count"] = cols

edf.sort_values("count", inplace=True, ascending=False)


def edf_find(genre):
    return edf[edf["g1"] == genre]


if __name__ == "__main__":
    graph.remove_nodes_from(g for g in genre_artists
                            if len(genre_artists[g]) <= 4)

    nx.draw_kamada_kawai(graph, with_labels=True, edge_color="g")
