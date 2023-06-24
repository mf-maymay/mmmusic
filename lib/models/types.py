from typing import Any, Callable, Optional

from lib.models.tracks import Track

Item = Any
Items = list[Item]

ItemPicker = Callable[[Items, Items, Item, Items], bool]
SeedPicker = Callable[[Items, Optional[Item]], tuple[Item, Item]]

Metrics = list[float]

Tracks = list[Track]
