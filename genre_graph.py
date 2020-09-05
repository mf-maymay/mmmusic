# -*- coding: utf-8 -*-
from collections import Counter, defaultdict
from itertools import permutations
import networkx as nx
import pandas as pd
from artists import get_genres
from users import User

user = User(input("username: "))

artist_genres = {}  # artist: genres of artist
genre_artists = defaultdict(set)  # genre: artists in genre
edges = Counter()  # (genre1, genre2): number of mutual artists

for artist in user.artists():
    artist_genres[artist] = get_genres(artist)

    for genre in get_genres(artist):
        genre_artists[genre].add(artist)

    edges.update(permutations(get_genres(artist), 2))

cogenres = pd.DataFrame()  # genres sharing artists (g1, g2, num_shared)
cols = list(zip(*((u, v, w) for (u, v), w in edges.items())))
cogenres["genre1"], cogenres["genre2"], cogenres["shared"] = cols
cogenres.sort_values("shared", inplace=True, ascending=False)


def draw_genre_map(size_min):
    """Draws a graph of genres connected by shared artists."""
    graph = nx.Graph()
    graph.add_edges_from(edges.keys())

    graph.remove_nodes_from(g for g in genre_artists
                            if len(genre_artists[g]) <= size_min)

    nx.draw_kamada_kawai(graph, with_labels=True, edge_color="gray",
                         style="dotted")


def related_genres(genre):
    return cogenres[cogenres["genre1"] == genre]


def genres_containing(keyword):
    return sorted(genre for genre in genre_artists if keyword in genre)


def artists_of_genres_containing(keyword):
    genres = genres_containing(keyword)
    seen = set()
    return [artist
            for genre in genres
            for artist in sorted(genre_artists[genre])
            if (artist not in seen and not seen.add(artist))]


if __name__ == "__main__":
    draw_genre_map(10)
