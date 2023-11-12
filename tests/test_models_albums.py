from datetime import date
import unittest
from unittest.mock import patch

from mmmusic.models.albums import Album, get_album


class TestArtist(unittest.TestCase):
    @patch("mmmusic.models.albums.spotify", autospec=True)
    def test_get_album(self, mock_spotify):
        fake_album_id = "fake_album_id"

        mock_spotify.get_album.return_value = {
            "name": "fake_name",
            "id": fake_album_id,
            "album_type": "album",
            "release_date": "1981-12",
            "artists": [{"id": "fake_artist_id"}],
        }

        album = get_album(fake_album_id)

        mock_spotify.get_album.assert_called_once_with(fake_album_id)

        self.assertEqual(
            album,
            Album(
                name="fake_name",
                id=fake_album_id,
                album_type="album",
                release_date=date(year=1981, month=12, day=1),
                artist_ids=("fake_artist_id",),
            ),
        )

    @patch("mmmusic.models.albums.spotify", autospec=True)
    def test_get_album_returns_album_as_is_when_supplied_album(self, mock_spotify):
        fake_album = Album(
            name="fake_name",
            id="fake_album_id",
            album_type="album",
            release_date=date(year=1981, month=12, day=1),
            artist_ids=("fake_artist_id",),
        )

        album = get_album(fake_album)

        mock_spotify.get_album.assert_not_called

        self.assertIs(album, fake_album)
