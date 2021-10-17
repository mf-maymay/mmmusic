# -*- coding: utf-8 -*-
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file
import matplotlib
from spotipy.exceptions import SpotifyException

from app_config import BASE_DIR
from artist import Artist
from artist_finder import grow_and_plot
from playlist_utils import shuffle_playlist
from user import User
from utils import no_timeout

Artist.use_json()

matplotlib.use("Agg")

app = Flask(__name__)


def _artist_id_from_input(_input):
    try:
        artist = Artist(_input)
    except SpotifyException:
        search_result = no_timeout(Artist._sp.search)(_input, limit=1, type="artist")
        artist = Artist(info=search_result["artists"]["items"][0])
    return artist.id


@app.route("/connect-artists", methods=("GET", "POST"))
def finder():
    if request.method == "POST":
        inputs = request.form["artist_1"], request.form["artist_2"]

        seeds = sorted(_artist_id_from_input(_input) for _input in inputs)

        return redirect("/connect-artists/" + "/".join(seeds))

    return render_template("finder_page.html")


@app.route("/connect-artists/<path:varargs>")
def finder_output(varargs=None):
    if varargs is None:
        return ""
    seeds = sorted(varargs.split("/"))
    file = BASE_DIR / Path("output") / ("-".join(seeds) + ".png")
    try:
        return send_file(file)
    except Exception:
        graph, (fig, ax) = grow_and_plot(*seeds, save=file)  # XXX
        return send_file(file)


@app.route("/shuffle", methods=("GET", "POST"))
def shuffle_page():
    if request.method == "POST":
        username = request.form["username"]
        playlist_id = request.form["playlist_id"]

        user = User(username)
        shuffle_playlist(user, playlist_id)

        return "<p>Done!</p>"

    return render_template("shuffle_page.html")
