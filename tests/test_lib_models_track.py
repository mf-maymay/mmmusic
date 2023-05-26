import unittest
from unittest.mock import patch

from lib.models.tracks import Track, get_track


class TestArtist(unittest.TestCase):
    @patch("lib.models.tracks.spotify", autospec=True)
    def test_get_track(self, mock_spotify):
        fake_track_id = "fake_track_id"

        mock_spotify.get_track.return_value = {
            "name": "fake_name",
            "id": "fake_track_id",
            "album": {"id": "fake_album_id"},
            "artists": [{"id": "fake_artist_id"}],
            "popularity": 50,
        }

        track = get_track(fake_track_id)

        mock_spotify.get_track.assert_called_once_with(fake_track_id)

        self.assertEqual(
            track,
            Track(
                name="fake_name",
                id="fake_track_id",
                album_id="fake_album_id",
                artist_ids=("fake_artist_id",),
                popularity=50,
            ),
        )

    @patch("lib.models.tracks.spotify", autospec=True)
    def test_get_track_returns_track_as_is_when_supplied_track(self, mock_spotify):
        fake_track = Track(
            name="fake_name",
            id="fake_track_id",
            album_id="fake_album_id",
            artist_ids=("fake_artist_id",),
            popularity=50,
        )

        track = get_track(fake_track)

        mock_spotify.get_track.assert_not_called

        self.assertIs(track, fake_track)
