from functools import reduce
from operator import and_

import pydantic

from mmmusic.models.types import TrackListTransformer
from mmmusic.shuffling import smart_shuffle
from mmmusic.track_sources import TrackSource, from_saved_albums


class PlaylistConfig(pydantic.BaseModel, arbitrary_types_allowed=True, extra="forbid"):
    id: str | None = None
    name: str
    description: str | None = None
    track_source: TrackSource = from_saved_albums
    order_tracks_func: TrackListTransformer = smart_shuffle
    track_list_processors: list[TrackListTransformer] = []
    _combined_processor: TrackListTransformer | None = None

    @property
    def combined_processor(self) -> TrackListTransformer:
        if self._combined_processor is None:
            self._combined_processor = reduce(
                and_,
                (*self.track_list_processors, self.order_tracks_func),
            )

        return self._combined_processor

    @pydantic.model_validator(mode="after")
    def fill_in_description(self):
        if self.description is None:
            if self.combined_processor is None:
                self.description = ""
            else:
                self.description = self.combined_processor.display_name

        return self
