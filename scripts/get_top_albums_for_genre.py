import numpy as np
import pandas as pd
from tabulate import tabulate

from mmmusic.external.everynoise import get_artists_for_genre
from mmmusic.external.sputnik import get_artist_albums


def get_score_confidence_levels(votes: np.ndarray) -> np.ndarray:
    return np.emath.logn(5, votes).astype(int)


def get_genre_album_ratings_dataframe(genre: str) -> pd.DataFrame:
    artists = get_artists_for_genre(genre)

    artist_albums = {artist: get_artist_albums(artist) for artist in artists}

    ratings = (
        pd.DataFrame(sum(artist_albums.values(), []))
        .rename(columns={"name": "album"})
        .dropna()
    )

    if ratings.empty:
        raise RuntimeError(f"No ratings were found for the {genre!r} albums.")

    ratings["confidence level"] = get_score_confidence_levels(ratings["votes"])

    ratings.sort_values(
        ["confidence level", "rating", "votes"],
        ascending=False,
        ignore_index=True,
        inplace=True,
    )

    return ratings


if __name__ == "__main__":
    genre = input("Genre: ")
    min_rating = float(input("Minimum rating: "))

    df = get_genre_album_ratings_dataframe(genre)

    filtered_df = df[
        (df["confidence level"] > 0) & (df["rating"] >= min_rating)
    ].reset_index(drop=True)

    print("\nTop albums:")  # noqa: T201
    print(tabulate(filtered_df, headers="keys", tablefmt="outline"))  # noqa: T201
