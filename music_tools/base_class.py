# -*- coding: utf-8 -*-
import atexit
import json
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyObjectBase:
    FIELDS: tuple

    __all_objects = {}  # XXX

    _sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(), retries=None)

    use_name_for_repr = False  # Use to replace default repr with name.

    def __init__(self, id=None, *, info=None):
        # Skip already-initialized objects.
        if hasattr(self, "id"):
            return

        self.info = info if info else self.full_response(id)
        self.id = self.info["id"]
        self.name = self.info["name"]

    def __new__(cls, id=None, *, info=None):  # TODO: kwargs
        if id is None and info is None:
            raise ValueError("Must supply either id or info")

        key = id if id is not None else info["id"]

        if key not in cls._objects():
            cls._objects()[key] = super().__new__(cls)

        return cls._objects()[key]

    @classmethod
    def full_response(cls, id):
        raise NotImplementedError

    @classmethod
    def _objects(cls):
        if cls not in SpotifyObjectBase.__all_objects:
            SpotifyObjectBase.__all_objects[cls] = {}
        return SpotifyObjectBase.__all_objects[cls]  # XXX

    @classmethod
    def _json_path(cls, base_dir: Path):
        return (base_dir / "objects" / f"{cls.__name__}.json").absolute()

    @classmethod
    def dump_to_json(cls, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(".")

        objects_to_dump = [_object.info for _object in cls._objects().values()]

        json_path = cls._json_path(base_dir)

        json_path.parent.mkdir(parents=True, exist_ok=True)  # XXX

        with open(json_path, "w") as json_file:
            json.dump(objects_to_dump, json_file)

    @classmethod
    def load_from_json(cls, base_dir: Path = None, *, ok_if_missing=False):
        if base_dir is None:
            base_dir = Path(".")

        json_path = cls._json_path(base_dir)

        if ok_if_missing and not json_path.is_file():
            json_objects = ()
        else:
            with open(json_path) as json_file:
                json_objects = json.load(json_file)  # list of objects

        for json_object in json_objects:
            # Implicitly create object in cache from info.
            cls(info=json_object)

    @classmethod
    def use_json(cls, base_dir: Path = None, *, ok_if_missing=False):
        if base_dir is None:
            base_dir = Path(".")

        cls.load_from_json(base_dir, ok_if_missing=ok_if_missing)

        atexit.register(cls.dump_to_json, base_dir)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, key):
        return self.info[key]

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name < str(other)

    def __repr__(self):
        return (
            self.name
            if self.use_name_for_repr
            else "{}({})".format(
                type(self).__name__,
                ", ".join(f"{field}={getattr(self, field)!r}" for field in self.FIELDS),
            )
        )

    def __str__(self):
        return self.name