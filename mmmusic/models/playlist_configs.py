from functools import cached_property, reduce
from operator import and_

from pydantic import BaseModel, computed_field, model_validator

from mmmusic.models.types import TrackListTransformer
from mmmusic.track_sources import TrackSource, from_saved_albums


class PlaylistConfig(BaseModel, arbitrary_types_allowed=True, extra="forbid"):
    id: str | None = None
    name: str
    description: str | None = None
    track_source: TrackSource = from_saved_albums
    processors: list[TrackListTransformer] = []

    @computed_field
    @cached_property
    def combined_processor(self) -> TrackListTransformer | None:
        if not self.processors:
            return None

        return reduce(and_, self.processors)

    @model_validator(mode="after")
    def fill_in_description(self):
        if self.description is None:
            if self.combined_processor is None:
                self.description = ""
            else:
                self.description = self.combined_processor.display_name

        return self
