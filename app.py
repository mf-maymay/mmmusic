# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

from playlist_utils import shuffle_playlist
from user import User

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def hello_world():
    if request.method == "POST":
        username = request.form["username"]
        playlist_id = request.form["playlist_id"]

        user = User(username)
        shuffle_playlist(user, playlist_id)

        return "<p>Done!</p>"

    return render_template("shuffle_page.html")
