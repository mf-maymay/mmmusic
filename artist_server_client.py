# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import Artist


c = Client(("localhost", 25000))

c.send("0oSGxfWSnnOXhD2fKuz2Gy")

artist_info = c.recv()

artist = Artist(info=artist_info)
