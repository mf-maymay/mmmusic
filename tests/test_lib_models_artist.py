import unittest
from unittest.mock import patch

from mmmusic.models.artists import Artist, get_artist


class TestArtist(unittest.TestCase):
    @patch("mmmusic.models.artists.spotify", autospec=True)
    def test_get_artist(self, mock_spotify):
        fake_artist_id = "fake_artist_id"

        mock_spotify.get_artist.return_value = {
            "name": "fake_name",
            "id": fake_artist_id,
            "genres": ("fake_genre",),
            "popularity": 50,
        }

        artist = get_artist(fake_artist_id)

        mock_spotify.get_artist.assert_called_once_with(fake_artist_id)

        self.assertEqual(
            artist,
            Artist(
                name="fake_name",
                id=fake_artist_id,
                genres=("fake_genre",),
                popularity=50,
            ),
        )

    @patch("mmmusic.models.artists.spotify", autospec=True)
    def test_get_artist_returns_artist_as_is_when_supplied_artist(self, mock_spotify):
        fake_artist = Artist(
            name="fake_name",
            id="fake_artist_id",
            genres=("fake_genre",),
            popularity=50,
        )

        artist = get_artist(fake_artist)

        mock_spotify.get_artist.assert_not_called

        self.assertIs(artist, fake_artist)
