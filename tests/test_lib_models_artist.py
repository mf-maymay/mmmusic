import unittest
from unittest.mock import patch

from lib.models.artist import Artist, get_artist


class TestArtist(unittest.TestCase):
    @patch("lib.models.artist.spotify", autospec=True)
    def test_get_artist(self, mock_spotify):
        fake_artist_id = "fake_artist_id"

        mock_spotify.get_artist.return_value = fake_artist = Artist(
            name="fake_name",
            id=fake_artist_id,
            genres=("fake_genre",),
            popularity=50,
        )

        artist = get_artist(fake_artist_id)

        mock_spotify.get_artist.assert_called_once_with(fake_artist_id)

        self.assertEqual(artist, fake_artist)

    @patch("lib.models.artist.spotify", autospec=True)
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
