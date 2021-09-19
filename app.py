# -*- coding: utf-8 -*-
from pathlib import Path

from flask import Flask, render_template, request, send_file

from artist_finder import grow_and_plot
from playlist_utils import shuffle_playlist
from user import User

app = Flask(__name__)


@app.route("/finder/<path:varargs>")
def finder_pager(varargs=None):
    if varargs is None:
        return ""
    seeds = sorted(varargs.split("/"))
    file = Path("output") / ("-".join(seeds) + ".png")
    if not file.is_file():
        graph, plot = grow_and_plot(*seeds, save=True)  # XXX
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
