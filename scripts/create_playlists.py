from mmmusic.data import playlist_configs
from mmmusic.playlists.generated_playlists import GeneratedPlaylist
from mmmusic.users import User
from mmmusic.utils import time_and_note_when_done

if __name__ == "__main__":
    user = User()

    playlists = {
        playlist_config.name: GeneratedPlaylist(config=playlist_config, user=user)
        for playlist_config in playlist_configs.regular_playlists
    }

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]

        print(f"\nGetting '{playlist.name}' tracks...")
        with time_and_note_when_done():
            playlist.get_tracks()

        if playlist.id is None:
            print(f"Creating '{playlist.name}'...")
            with time_and_note_when_done():
                playlist.create()
        else:
            print(f"Recreating '{playlist.name}'...")
            with time_and_note_when_done():
                playlist.recreate()
