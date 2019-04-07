# -*- coding: utf-8 -*-
import pandas as pd
import spotipy
from credentials import token

exclude = {"Freaky", "Rockabye Baby!", "Various Artists"}

sp = spotipy.Spotify(auth=token)
all_artists = set()
offset = 0
while True:
    albums = sp.current_user_saved_albums(limit=50, offset=offset)
    items = albums["items"]
    for item in items:
        all_artists |= {(artist["name"], artist["id"])
                        for artist in item["album"]["artists"]
                        if artist["name"] not in exclude}
    offset += len(items)
    if len(items) == 0:
        break

all_artists = sorted(all_artists)


def get_data(excel=False):
    df = pd.DataFrame()

    df["name"], df["id"] = list(zip(*all_artists))

    df["popularity"] = [sp.artist(k)["popularity"] for k in df["id"]]

    df.sort_values("popularity", ascending=False, inplace=True)

    if excel:
        df.to_excel("artists.xlsx", index=False)

    return df
