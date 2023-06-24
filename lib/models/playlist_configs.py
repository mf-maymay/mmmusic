import pydantic

from lib.models.types import TrackListTransformer
from lib.shuffling import smart_shuffle


class PlaylistConfig(pydantic.BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    order_tracks_func: TrackListTransformer = smart_shuffle
    track_filters: list[TrackListTransformer] = []
