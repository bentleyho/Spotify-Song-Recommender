import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pandas import DataFrame
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import os
from IPython.core.display import HTML

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
        scope="playlist-modify-public user-library-read user-read-playback-state",
        cache_path=".spotifycache",
    )

def get_track_id(track_name, artist_name):
    results = spotify.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    items = results['tracks']['items']
    if items:
        return items[0]['id']
    else:
        return None

def img_html(url):
    return f'<img src="{url}" width="50" >'

def preview_html(url):
    if url:
        return f'<a href="{url}">Listen on Spotify</a>'
    else:
        return 'N/A'

def create_playlist(track_ids, token_info, playlist_name):
    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)

    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_ids)

    return playlist['external_urls']['spotify']

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
            track_ids = []
            if "tracks" in recommendations:
                for track in recommendations["tracks"]:
                    recommended_tracks.append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "popularity": track["popularity"],
                        "preview_url": preview_html(track["preview_url"]),
                        "album_art": img_html(track["album"]["images"][0]["url"])
                    })
                    track_ids.append(track["id"])

            playlist_name = f"{track_name} by {artist_name} Recommended Playlist"

            if 'token_info' in session:
                playlist_url = create_playlist(track_ids, session['token_info'], playlist_name) if track_ids else None
                response = {
                    "track_id": track_id,
                    "track_name": track_name,
                    "artist_name": artist_name,
                    "features": audio_features[0] if audio_features else None,
                    "seed_track_name": seed_track_name,
                    "recommendations": recommended_tracks,
                    "playlist_url": playlist_url
                }
            else:
                sp_oauth = spotify_oauth()
                auth_url = sp_oauth.get_authorize_url()
                session['track_ids'] = track_ids
                session['playlist_name'] = playlist_name
                response = {"auth_url": auth_url}

        else:
            response = {
                "track_id": None,
                "track_name": track_name,
                "artist_name": artist_name,
                "features": None,
                "seed_track_name": None,
                "recommendations": [],
                "playlist_url": None
            }

        # Create DataFrame and render as HTML
        if 'recommendations' in response and response['recommendations']:
            records = []
            for index, track in enumerate(response['recommendations']): 
                record = {
                    "Track": index,
                    "Name": track['name'],
                    "Artist": track["artist"],
                    "Popularity": track["popularity"],
                    "Preview URL": track["preview_url"],
                    "Album Art": track["album_art"]
                }
                records.append(record)

            tracks_df = DataFrame(records)
            tracks_table = HTML(tracks_df.to_html(escape=False, index=False, formatters=dict(album_art=lambda x: x, preview_url=lambda x: x)))

            response['html_table'] = tracks_table.data

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spotify_routes.route('/auth/spotify/callback')
def spotify_callback():
    sp_oauth = spotify_oauth()
    session.clear()
    token_info = sp_oauth.get_access_token(request.args['code'])
    session["token_info"] = token_info

    if 'track_ids' in session:
        track_ids = session['track_ids']
        playlist_name = session['playlist_name']
        playlist_url = create_playlist(track_ids, token_info, playlist_name)
        return redirect(url_for('spotify_routes.track_details', playlist_url=playlist_url))

    return redirect(url_for('spotify_routes.track_details'))

@spotify_routes.route('/track_details', methods=['GET'])
def track_details():
    playlist_url = request.args.get('playlist_url', None)
    return render_template('track_details.html', playlist_url=playlist_url)
