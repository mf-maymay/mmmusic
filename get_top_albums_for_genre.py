import numpy as np
import pandas as pd

from lib.external.everynoise import get_artists_for_genre
from lib.external.sputnik import get_artist_albums


def get_score_confidence_levels(votes: np.ndarray) -> np.ndarray:
    return np.emath.logn(5, votes).astype(int)


def get_genre_album_ratings_dataframe(genre: str) -> pd.DataFrame:
    artists = get_artists_for_genre(genre)

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

    return ratings


if __name__ == "__main__":
    genre = input("Genre: ")

    df = get_genre_album_ratings_dataframe(genre)

    filtered_df = df[(df["confidence level"] > 0) & (df["rating"] > 4)]

    print("Top albums:")
    for _, row in filtered_df.iterrows():
        print(
            f"- {row['album']!r} by {row['artist']}: {row['rating']} rating "
            f"(votes: {row['votes']:,}, confidence level: {row['confidence level']})"
        )