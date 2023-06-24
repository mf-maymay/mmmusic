from typing import Callable

import pydantic

from lib.models.types import TrackListTransformer, Tracks
from lib.shuffling import smart_shuffle
from lib.users import User


class PlaylistConfig(pydantic.BaseModel):
    id: str | None
    name: str
    description: str = ""
    track_source: Callable[[User], Tracks] = User.get_tracks_from_saved_albums
    order_tracks_func: TrackListTransformer = smart_shuffle
    track_filters: list[TrackListTransformer] = []

    class Config:
        extra = pydantic.Extra.forbid
