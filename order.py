# -*- coding: utf-8 -*-
import networkx as nx
from artist import Artist


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
