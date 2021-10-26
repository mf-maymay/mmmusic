# -*- coding: utf-8 -*-
import multiprocessing
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file
import matplotlib

from app_config import BASE_DIR
from artist import Artist, search_for_artist
from artist_finder import grow_and_plot
from playlist_utils import shuffle_playlist
from user import User

Artist.use_json(BASE_DIR)

matplotlib.use("Agg")

app = Flask(__name__)


@app.route("/connect-artists", methods=("GET", "POST"))
def finder():
    if request.method == "POST":
        inputs = request.form["artist_1"], request.form["artist_2"]

        seeds = sorted(search_for_artist(_input).id for _input in inputs)

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
        process = multiprocessing.Process(
            target=grow_and_plot, args=seeds, kwargs={"save": file}
        )
        process.start()
        return '<meta http-equiv="refresh" content="300">'


@app.route("/shuffle", methods=("GET", "POST"))
def shuffle_page():
    if request.method == "POST":
        username = request.form["username"]
        playlist_id = request.form["playlist_id"]

        user = User(username)
        shuffle_playlist(user, playlist_id)

        return "<p>Done!</p>"

    return render_template("shuffle_page.html")
