from mmmusic.logging import get_logger
from mmmusic.models.tracks import get_track
from mmmusic.shuffling import smart_shuffle
from mmmusic.users import User
from mmmusic.utils import take_x_at_a_time

logger = get_logger()

MAX_TRACKS = 11_000


def add_tracks_to_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    if len(tracks) > MAX_TRACKS:
        logger.warning(
            f"Playlist has {len(tracks):,} tracks. "
            f"Only the first {MAX_TRACKS:,} will be included."
        )

    for to_add in take_x_at_a_time(tracks[:MAX_TRACKS], 100):
        user.sp.user_playlist_add_tracks(user.username, playlist_id, to_add)


def clear_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    remove_tracks_from_playlist(playlist_id, tracks=tracks, user=user)


def create_playlist(*, public=False, name, description, user: User) -> str:
    response = user.sp.user_playlist_create(
        user.username, name, public=public, description=description
    )

    return response["id"]


def get_tracks_from_playlist(playlist_id, *, user: User):
    tracks = []

    logger.debug("Getting tracks from playlist %r", playlist_id)

    items = user.sp.playlist_items(playlist_id)

    while items:
        tracks.extend(get_track(item["track"]["id"]) for item in items["items"])
        items = user.sp.next(items)

        if items:
            logger.debug("Getting more tracks from playlist %r", playlist_id)

    return tracks


def remove_tracks_from_playlist(playlist_id, *, tracks, user: User):
    tracks = [track if isinstance(track, str) else track.id for track in tracks]

    for to_remove in take_x_at_a_time(tracks, 100):
        user.sp.user_playlist_remove_all_occurrences_of_tracks(
            user.username, playlist_id, to_remove
        )


def replace_playlist(
    playlist_id,
    *,
    new_tracks,
    user: User,
    new_name: str | None = None,
    new_description: str | None = None,
):
    if not new_description:
        new_description = None

    clear_playlist(playlist_id, user=user)

    add_tracks_to_playlist(playlist_id, tracks=new_tracks, user=user)

    # NOTE: The Spotify API does not accept null or empty descriptions.
    if not new_description:
        new_description = None

    if new_name or new_description:
        user.sp.user_playlist_change_details(
            user=user.username,
            playlist_id=playlist_id,
            name=new_name,
            description=new_description,
        )


def shuffle_playlist(playlist_id, *, user: User):
    tracks = get_tracks_from_playlist(playlist_id, user=user)

    shuffled = smart_shuffle(tracks)

    replace_playlist(playlist_id, new_tracks=shuffled, user=user)
