# -*- coding: utf-8 -*-
from album import Album
from artist import Artist
from genre_graph import artists_of_genres_containing
from shuffling import order_tracks
from user import User
from utils import create_playlist, no_timeout, record_calls

# -------
# keywords, playlist_name = ["goth"], "goth"
# keywords, playlist_name = ["black"], "black"
# keywords, playlist_name = ["japan", "j-"], "japan"
# keywords, playlist_name = ["americana", "country"], "american"
# keywords, playlist_name = ["blue"], "blue"
keywords, playlist_name = ["metal"], "mettle"
# keywords, playlist_name = ["classical"], "classicle"
# keywords, playlist_name = ["bop"], "bop"
# keywords, playlist_name = ["punk"], "pink"
# keywords, playlist_name = ["hop"], "hops"
# keywords, playlist_name = ["jazz"], "jazzistico"
# -------

Artist._use_name_for_repr = True

Album.tracks = no_timeout(Album.tracks)
Artist.related = record_calls(no_timeout(Artist.related))
User.artists = no_timeout(User.artists)

user = User(input("username: "))

artists = set()
for keyword in keywords:
    artists |= artists_of_genres_containing(keyword, user.artists())

albums = {album for album in user.albums() if set(album.artist_ids) & artists}

artist_albums = {artist: sorted((album for album in albums
                                 if artist in album.artist_ids),
                                key=Album.release_date)
                 for artist in artists}

albums_order = []
tracks = []

for artist in artists:
    for album in artist_albums[artist]:
        if album not in albums_order:
            albums_order.append(album)
            tracks.extend(track["id"] for track in album.tracks())

ordered = order_tracks(tracks, user)

# -------

create_playlist(user, ordered, playlist_name)
