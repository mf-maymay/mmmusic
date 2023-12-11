from mmmusic.data import playlist_configs
from mmmusic.playlists.generated_playlists import GeneratedPlaylist
from mmmusic.users import User

if __name__ == "__main__":
    user = User()

    playlists = {
        playlist_config.name: GeneratedPlaylist(config=playlist_config, user=user)
        for playlist_config in playlist_configs.regular_playlists
    }

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]

        playlist.get_tracks()

        if playlist.id is None:
            playlist.create()
        else:
            playlist.recreate()
