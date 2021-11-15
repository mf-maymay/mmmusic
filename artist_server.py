# -*- coding: utf-8 -*-
from multiprocessing.connection import Listener
import traceback

from music_tools.artist import Artist


def return_artists(conn):
    try:
        while True:
            artist_id = conn.recv()
            print("artist_id:", artist_id)

            artist = Artist(artist_id)

            print("artist:", repr(artist))

            conn.send(Artist(artist_id).info)

    except EOFError:
        print("Connection closed")


def echo_server(address):
    serv = Listener(address)
    while True:
        try:
            client = serv.accept()
            return_artists(client)
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    echo_server(("", 25000))
