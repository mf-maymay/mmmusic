from functools import reduce
from operator import and_

import pydantic

from mmmusic.models.types import TrackListTransformer
from mmmusic.track_sources import TrackSource, from_saved_albums


class PlaylistConfig(pydantic.BaseModel, arbitrary_types_allowed=True, extra="forbid"):
    id: str | None = None
    name: str
    description: str | None = None
    track_source: TrackSource = from_saved_albums
    processors: list[TrackListTransformer] = []

    _combined_processor: TrackListTransformer | None = None

    @property
    def combined_processor(self) -> TrackListTransformer | None:
        if self._combined_processor is None and self.processors:
            self._combined_processor = reduce(and_, self.processors)

        return self._combined_processor

    @pydantic.model_validator(mode="after")
    def fill_in_description(self):
        if self.description is None:
            if self.combined_processor is None:
                self.description = ""
            else:
                self.description = self.combined_processor.display_name

        return self
