import pytest
from app.clientIDSecret import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pandas import DataFrame

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_id(track_name, artist_name):
    results = spotify.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    items = results['tracks']['items']
    if items:
        return items[0]['id']
    else:
        return None

def test_get_track_id():
    # Test with a known track
    track_id = get_track_id('Off My Face', 'Justin Bieber')
    assert track_id is not None, "Track ID should not be None for a known track"
    
    # Test with a non-existent track
    track_id = get_track_id('Mocking Bird', 'Justin Beiber')
    assert track_id is None, "Track ID should be None for a non-existent track"