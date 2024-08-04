# IMPORTS
# packages (require installation)
import spotipy
import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.core.display import HTML
from spotipy.oauth2 import SpotifyOAuth
from pandas import DataFrame
from dotenv import load_dotenv

#ENVIRONMENT VARIABLE RELATED CODE:

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = client_credentials_manager.get_access_token(as_dict=False)


def get_track_id(track_name, artist_name):
    results = spotify.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    items = results['tracks']['items']
    if items:
        return items[0]['id']
    else:
        return None

u = input("Please type the Song Name:").strip()
z = input("Please type the Artist Name:").strip()
track_name = u
artist_name = z
track_id = get_track_id(track_name, artist_name)

if track_id:
    print(f'Track ID for "{track_name}" by {artist_name}: {track_id}')
else:
    print(f'Track "{track_name}" by {artist_name} not found.')

audio_features = spotify.audio_features(track_id)

if audio_features:
    features = audio_features[0]
    print(features)
else:
    print("Track not found or no features available.")

seed_track = spotify.track(track_id)

seed_track_name = seed_track["name"]


recommendations = spotify.recommendations(seed_tracks=[track_id])

if "tracks" in recommendations:
    recommended_tracks = recommendations["tracks"]
    if len(recommended_tracks) > 0:
        print(f"Songs similar to '{seed_track_name}':")
        for track in recommended_tracks:
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            print(f"Track: {track_name} - Artist: {artist_name}")
    else:
        print("No recommendations found.")
else:
    print("Recommendations not available.")