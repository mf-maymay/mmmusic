import numpy as np
import pandas as pd

from lib.external.everynoise import get_artists_for_genre
from lib.external.sputnik import get_artist_albums


def get_score_confidence_levels(votes: np.ndarray) -> np.ndarray:
    return np.emath.logn(5, votes).astype(int)


artists = get_artists_for_genre("heavypsych")

artist_albums = {artist: get_artist_albums(artist) for artist in artists}

ratings = (
    pd.DataFrame(sum(artist_albums.values(), []))
    .rename(columns={"name": "album"})
    .dropna()
    .sort_values(["rating", "votes"], ascending=False, ignore_index=True)
)

ratings["confidence level"] = get_score_confidence_levels(ratings["votes"])

ratings.sort_values(
    "confidence level", ascending=False, ignore_index=True, inplace=True
)
