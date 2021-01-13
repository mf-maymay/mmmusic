# -*- coding: utf-8 -*-
import networkx as nx
from artist import Artist
from artist_finder import grow, trim, paths_subgraph


def dfs_order(artists, source=None, full=False):
    artists = {Artist(artist) for artist in artists}

    G = nx.Graph()  # undirected
    G.add_nodes_from(artists)

    for artist in artists:
        related = set(artist.related())

        for rel in related & artists:  # related artists within library
            G.add_edge(artist, rel)

    if source is None:
        source = max(G.nodes, key=G.degree)  # most connected

    dfs_edges = tuple(nx.dfs_edges(G, source=source))
    seen = set()
    dfs = [node for node, _ in dfs_edges
           if node not in seen and not seen.add(node)]

    if not dfs_edges:
        dfs.append(source)

    if full:
        while (G.remove_node(source) or
               G.remove_edges_from(dfs_edges) or
               G):

            source = max(G.nodes, key=G.degree)  # most connected

            dfs_edges = tuple(nx.dfs_edges(G, source=source))
            seen = set(dfs)
            dfs.extend(node for node, _ in dfs_edges
                       if node not in seen and not seen.add(node))

            if not dfs_edges and source not in seen:
                dfs.append(source)

    return dfs


def greedy_order(artists, paths=None, log=False):
    if paths is None:
        graph = grow(artists)
        graph = trim(graph, keepers=artists)
        graph, paths = paths_subgraph(graph, artists)

    # path_lens = lengths of shortest paths between pairs
    path_lens = {pair: len(paths[pair][0]) for pair in paths}

    greedy = [min(artists, key=lambda a: a.popularity)]

    if log:
        print(greedy[0])

    short = nx.Graph()

    short.add_weighted_edges_from((*p, w) for p, w in path_lens.items())

    while short.edges:
        closest = min(short[greedy[-1]],
                      key=lambda n: (short.edges[greedy[-1], n]["weight"],
                                     n.popularity))  # closest, least popular
        short.remove_node(greedy[-1])
        greedy.append(closest)
        if log:
            print(closest)

    return greedy


if __name__ == "__main__":
    from artist_ids import ids
    from user import User

    user = User(input("username: "))

    # source = None
    # full = True

    source = Artist(ids["owls"])
    full = False

    dfs = dfs_order(user.artists(), source=source, full=full)

    for artist in dfs:
        print(artist)
