from mmmusic.features import get_scores_for_tracks, similarity
from mmmusic.models.tracks import Track

Seed = Track


def by_similarity(
    *,
    seed: Seed,
    tracks: list[Track],
) -> list[Track]:
    scores = get_scores_for_tracks([*tracks, seed])

    similarities: dict[Track, float] = {
        track: similarity(scores[track], scores[seed]) for track in tracks
    }

    return sorted(tracks, key=similarities.get, reverse=True)
