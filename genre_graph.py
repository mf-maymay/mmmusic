# -*- coding: utf-8 -*-
from collections import Counter, defaultdict
from itertools import permutations
import networkx as nx
import pandas as pd
from artist_info import saved
from utils import get_genres

artist_genres = {}
genre_artists = defaultdict(list)
edges = Counter()


for artist, name in saved.items():
    artist_genres[name] = get_genres(artist)

    for genre in get_genres(artist):
        genre_artists[genre].append(name)

    edges.update(permutations(get_genres(artist), 2))


graph = nx.Graph()
graph.add_edges_from(edges.keys())


edf = pd.DataFrame()

cols = list(zip(*((u, v, w) for (u, v), w in edges.items())))

edf["g1"], edf["g2"], edf["count"] = cols

edf.sort_values("count", inplace=True, ascending=False)


def edf_find(genre):
    return edf[edf["g1"] == genre]
