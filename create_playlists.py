from lib.data.playlist_configs import playlist_configs
from lib.playlists import GeneratedPlaylist
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User
from lib.utils import time_and_note_when_done


if __name__ == "__main__":
    user = User()

    playlists = {
        playlist_config.name: GeneratedPlaylist(config=playlist_config, user=user)
        for playlist_config in playlist_configs
    }

    to_create = sorted(playlists)

    for key in to_create:
        playlist = playlists[key]

        with time_and_note_when_done(f"\nGetting '{playlist.name}' tracks..."):
            playlist.get_tracks()

        if playlist.id is not None and set(
            get_tracks_from_playlist(playlist.id, user=user)
        ) == set(playlist.tracks):
            print(
                f"Skipping processing for '{playlist.name}' "
                f"because its tracks have not changed."
            )
            continue

        with time_and_note_when_done(f"Ordering '{playlist.name}' tracks..."):
            playlist.order_tracks()

        if playlist.id is None:
            with time_and_note_when_done(f"Creating '{playlist.name}'..."):
                playlist.create()
        else:
            with time_and_note_when_done(f"Recreating '{playlist.name}'..."):
                playlist.recreate()
