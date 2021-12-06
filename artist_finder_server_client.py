# -*- coding: utf-8 -*-
from multiprocessing.connection import Client

from music_tools.artist import search_for_artist

c = Client(("localhost", 25000))

c.send([search_for_artist("alice coltrane").id, search_for_artist("sun ra").id])

# response = c.recv()  # XXX
