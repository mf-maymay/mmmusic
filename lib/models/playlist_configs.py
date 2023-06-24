from typing import Callable

import pydantic

from lib.models.types import TrackListTransformer, Tracks
from lib.shuffling import smart_shuffle


class PlaylistConfig(pydantic.BaseModel):
    id: str | None
    name: str
    description: str = ""
    track_source: Callable[[], Tracks] | None
    order_tracks_func: TrackListTransformer = smart_shuffle
    track_filters: list[TrackListTransformer] = []
