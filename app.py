# -*- coding: utf-8 -*-
import os
from pathlib import Path
import subprocess
import sys

from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
import matplotlib

from app_config import BASE_DIR
from music_tools.artist import Artist, search_for_artist
from music_tools.playlist_utils import shuffle_playlist
from music_tools.user import User

Artist.load_from_json()

matplotlib.use("Agg")

app = Flask(__name__)

app.secret_key = os.environ["SPOTIFY_APP_SECRET_KEY"]


@app.route("/radio")
def radio():
    def generate():  # XXX
        for mp3 in (BASE_DIR / "radio_songs").glob("*.mp3"):
            with open(mp3, "rb") as f:
                data = f.read(1024)
                while data:
                    yield data
                    data = f.read(1024)

    return Response(generate(), mimetype="audio/mpeg")


@app.route("/connect-artists", methods=("GET", "POST"))
def finder_home():
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
def shuffle_home():
    if "username" not in session:
        return redirect(url_for("login"))  # XXX

    if request.method == "POST":
        playlist_id = request.form["playlist_id"]

        user = User(session["username"])

        session["token_info"] = user.sp.auth_manager.get_access_token(
            session["auth_code"]
        )  # XXX

        shuffle_playlist(user, playlist_id)

        return "Done!"

    return render_template("shuffle_page.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]

        user = User(session["username"])

        auth_url = user.sp.auth_manager.get_authorize_url()

        print("Authorization URL:", auth_url)

        return redirect(auth_url)

    return render_template("login_page.html")


@app.route("/api_callback", methods=("GET", "POST"))
def api_callback():
    session["auth_code"] = request.args.get("code")

    return redirect(url_for("shuffle_home"))  # XXX


@app.route("/logout")
def logout():
    session.pop("username", None)
    return "You are now logged out."
