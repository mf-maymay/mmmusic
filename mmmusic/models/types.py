from typing import Any, Callable, Optional

from mmmusic.models.tracks import Track

Item = Any
Items = list[Item]

ItemPicker = Callable[[Items, Items, Item, Items], bool]
SeedPicker = Callable[[Items, Optional[Item]], tuple[Item, Item]]

Metrics = list[float]

Tracks = list[Track]

TrackListTransformer = Callable[[Tracks], Tracks]
