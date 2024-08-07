# web_app/routes/spotify_routes.py

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pandas import DataFrame
from flask import Blueprint, request, jsonify, render_template
import os

from app.clientIDSecret import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

SPOTIPY_REDIRECT_URI = "http://localhost:5000/auth/spotify/callback"

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spotify_routes = Blueprint('spotify_routes', __name__)

def spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read user-read-playback-state",
        cache_path=".spotifycache",
    )

def get_track_id(track_name, artist_name):
    results = spotify.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    items = results['tracks']['items']
    if items:
        return items[0]['id']
    else:
        return None

@spotify_routes.route('/get_track_details', methods=['POST'])
def get_track_details():
    try:
        data = request.json
        track_name = data.get('track_name')
        artist_name = data.get('artist_name')

        if not track_name or not artist_name:
            return jsonify({'error': 'Missing track_name or artist_name'}), 400

        track_id = get_track_id(track_name, artist_name)

        if track_id:
            audio_features = spotify.audio_features(track_id)
            seed_track = spotify.track(track_id)
            seed_track_name = seed_track["name"]
            recommendations = spotify.recommendations(seed_tracks=[track_id])

            recommended_tracks = []
            if "tracks" in recommendations:
                for track in recommendations["tracks"]:
                    recommended_tracks.append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "popularity": track["popularity"],
                        "preview_url": preview_html(track["preview_url"]),
                        "album_art": img_html(track["album"]["images"][0]["url"])
                    })

            response = {
                "track_id": track_id,
                "track_name": track_name,
                "artist_name": artist_name,
                "features": audio_features[0] if audio_features else None,
                "seed_track_name": seed_track_name,
                "recommendations": recommended_tracks
            }
        else:
            response = {
                "track_id": None,
                "track_name": track_name,
                "artist_name": artist_name,
                "features": None,
                "seed_track_name": None,
                "recommendations": []
            }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def img_html(url):
    return '<img src="'+ url + '" width="50" >'

def preview_html(url):
    if url:
        return '<a href="'+ url + '" >Listen on Spotify</a>'
    else:
        return None

@spotify_routes.route('/track_details', methods=['GET'])
def track_details():
    return render_template('track_details.html')
