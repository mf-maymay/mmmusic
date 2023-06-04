from lib.models.tracks import get_track
from lib.shuffling import smart_shuffle
from lib.users import User
from lib.utils import no_timeout, take_x_at_a_time

MAX_TRACKS = 11_000


def add_tracks_to_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    if len(tracks) > MAX_TRACKS:
        print(
            f"Playlist has {len(tracks):,} tracks. Only adding first {MAX_TRACKS:,} ..."
        )

    for to_add in take_x_at_a_time(tracks[:MAX_TRACKS], 100):
        no_timeout(user.sp.user_playlist_add_tracks)(user.username, playlist_id, to_add)


def clear_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    remove_tracks_from_playlist(playlist_id, tracks=tracks, user=user)


def create_playlist(*, public=False, name, description, user: User) -> str:
    response = no_timeout(user.sp.user_playlist_create)(
        user.username, name, public=public, description=description
    )

    return response["id"]


def get_tracks_from_playlist(playlist_id, *, user: User):
    tracks = []

    items = no_timeout(user.sp.playlist_items)(playlist_id)

    while items:
        tracks.extend(get_track(item["track"]["id"]) for item in items["items"])
        items = no_timeout(user.sp.next)(items)

    return tracks


def remove_tracks_from_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_remove in take_x_at_a_time(tracks, 100):
        no_timeout(user.sp.user_playlist_remove_all_occurrences_of_tracks)(
            user.username, playlist_id, to_remove
        )


def replace_playlist(playlist_id, *, new_tracks, user: User):
    clear_playlist(playlist_id, user=user)

    add_tracks_to_playlist(playlist_id, tracks=new_tracks, user=user)


def shuffle_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    shuffled = smart_shuffle(tracks)

    replace_playlist(playlist_id, new_tracks=shuffled, user=user)
