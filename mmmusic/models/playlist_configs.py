import pydantic

from mmmusic.models.types import TrackListTransformer
from mmmusic.shuffling import smart_shuffle
from mmmusic.track_sources import TrackSource, from_saved_albums


class PlaylistConfig(pydantic.BaseModel):
    id: str | None = None
    name: str
    description: str = ""
    track_source: TrackSource = from_saved_albums
    order_tracks_func: TrackListTransformer = smart_shuffle
    track_filters: list[TrackListTransformer] = []

    class Config:
        extra = pydantic.Extra.forbid
