# -*- coding: utf-8 -*-
from pathlib import Path

from flask import Flask, render_template, request, send_file
import matplotlib

from app_config import BASE_DIR
from artist_finder import grow_and_plot
from playlist_utils import shuffle_playlist
from user import User

matplotlib.use("Agg")

app = Flask(__name__)


@app.route("/connect-artists/<path:varargs>")
def finder_output(varargs=None):
    print(varargs)
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
