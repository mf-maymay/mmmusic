import matplotlib.pyplot as plt
import numpy as np

from lib.genres import get_track_genre_attributes
from lib.playlists.management import get_tracks_from_playlist
from lib.users import User


def plot(xs, ys):
    fig, ax = plt.subplots()

    fig.set_facecolor("grey")
    ax.set_facecolor("lightgrey")

    ax.plot(xs, ys, "w", alpha=0.2, linewidth=0.5, zorder=1)

    ax.scatter(
        xs,
        ys,
        s=16,
        c=np.arange(len(xs)),
        cmap="cividis",
        linewidths=0.1,
        edgecolors="white",
        zorder=2,
    )

    # NOTE: Plenty of tracks have the same genre coordinates, so they get stacked.

    ax.set_xlabel("top")
    ax.set_ylabel("left")

    fig.tight_layout()

    return fig, ax


PLAYLIST_ID = "5AndDQTKOCzIuGM4fJhXnT"

user = User()

tracks = get_tracks_from_playlist(PLAYLIST_ID, user=user)

coordinate_pairs = np.array([get_track_genre_attributes(track) for track in tracks])

xs = coordinate_pairs[:, 0]
ys = coordinate_pairs[:, 1]

fig, ax = plot(xs, ys)

fig.show()
