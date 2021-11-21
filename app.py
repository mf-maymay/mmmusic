# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys

from flask import Flask, redirect, render_template, request, send_file
import matplotlib

from app_config import BASE_DIR
from music_tools.artist import Artist, RelatedArtists, search_for_artist
from music_tools.playlist_utils import shuffle_playlist
from music_tools.user import User

Artist.load_from_json(BASE_DIR)
RelatedArtists.load_from_json(BASE_DIR)

matplotlib.use("Agg")

app = Flask(__name__)


@app.route("/connect-artists", methods=("GET", "POST"))
def finder():
    if request.method == "POST":
        inputs = request.form["artist_1"], request.form["artist_2"]

        return redirect(
            "/connect-artists/"
            + "/".join(search_for_artist(_input).id for _input in inputs)
        )

    return render_template("finder_page.html")


@app.route("/connect-artists/<path:varargs>")
def finder_output(varargs=None):
    if varargs is None:
        return ""

    seeds = varargs.split("/")

    file = BASE_DIR / Path("output") / ("-".join(sorted(seeds)) + ".png")

    if file.is_file():
        if file.stat().st_size > 0:
            # Send file if it is ready.
            return send_file(file)
    else:
        # Create file if it does not exist.
        file.touch()  # Mark that file is being created.

        subprocess.Popen(
            [sys.executable, BASE_DIR / "artist_finder.py", *seeds, "-f", str(file)]
        )

    # Send loading page if file is not ready.
    artists = [Artist(seed) for seed in seeds]

    images = [
        None if not artist.info["images"] else artist.info["images"][0]["url"]
        for artist in artists
    ]

    return render_template(
        "loading_page.html",
        artist_1=artists[0],
        artist_2=artists[1],
        image_1=images[0],
        image_2=images[1],
    )


@app.route("/shuffle", methods=("GET", "POST"))
def shuffle_page():
    if request.method == "POST":
        username = request.form["username"]
        playlist_id = request.form["playlist_id"]

        user = User(username)
        shuffle_playlist(user, playlist_id)

        return "<p>Done!</p>"

    return render_template("shuffle_page.html")
