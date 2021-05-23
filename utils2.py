# -*- coding: utf-8 -*-


def albums_from_artists(user, artists):
    artists = set(artists)
    return sorted(
        {album for album in user.albums() if set(album.artist_ids) & artists}
    )


def tracks_from_albums(albums):
    return [track for album in albums for track in album.tracks()]


if __name__ == "__main__":
    from artist import Artist
    from user import User

    artists = [Artist("4Z8W4fKeB5YxbusRsdQVPb"),
               Artist("0oSGxfWSnnOXhD2fKuz2Gy")]

    user = User(input("username: "))

    albums = albums_from_artists(user, artists)

    tracks = tracks_from_albums(albums)
