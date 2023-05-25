import unittest
from unittest.mock import patch

from lib.external.spotify import get_artist


@patch("lib.external.spotify.get_client_credentials_managed_client", autospec=True)
class TestSpotify(unittest.TestCase):
    def test_get_artist(self, mock_get_client_credentials_managed_client):
        get_artist("fake_artist_id")

        mock_get_client_credentials_managed_client.return_value.artist.assert_called_once_with(
            "fake_artist_id"
        )
