# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import permutations
import networkx as nx
from artist import Artist


def genre_members(artists):
    """Returns a dictionary mapping genres to their artists."""
    genre_artists = defaultdict(set)  # genre: artists in genre

    for artist in artists:
        for genre in artist.genres:
            genre_artists[genre].add(artist)

    return genre_artists


def genres_containing(keyword, artists):
    """Returns the genres containing `keyword` in their names."""
    return {genre for genre in genre_members(artists) if keyword in genre}


def artists_of_genres_containing(keyword, artists):
    """Returns the artists of genres containing `keyword` in their names."""
    members = set()

    genre_artists = genre_members(artists)

    for genre in genres_containing(keyword, artists):
        members.update(genre_artists[genre])

    return members


def genre_overlaps(artists):
    """Returns a dictionary mapping pairs of genres to their shared artists."""
    mutuals = defaultdict(set)

    for artist in artists:
        for pair in permutations(Artist(artist).genres, 2):
            mutuals[pair].add(artist)

    return mutuals


def related_genres(genre, artists):
    """Returns the genres that share artists with `genre`."""
    related = set()

    for pair in genre_overlaps(artists):
        if genre in pair:
            related.update(pair)

    return related - {genre}


def genre_map(size_min, artists, draw=False):
    """Creates a graph of genres connected by shared artists."""
    graph = nx.Graph()
    graph.add_edges_from(genre_overlaps(artists))

    genre_artists = genre_members(artists)

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

    genre_artists = genre_members(artists)

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
