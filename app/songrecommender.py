# IMPORTS
# packages (require installation)
import spotipy # type: ignore
import requests
from spotipy.oauth2 import SpotifyClientCredentials # type: ignore
from IPython.core.display import HTML
from spotipy.oauth2 import SpotifyOAuth # type: ignore
from pandas import DataFrame

from app.clientIDSecret import SPOTIPY_CLIENT_ID
from app.clientIDSecret import SPOTIPY_CLIENT_SECRET


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


# convert image URL to html
# credit to: https://towardsdatascience.com/rendering-images-inside-a-pandas-dataframe-3631a4883f60

def img_html(url):
    return '<img src="'+ url + '" width="50" >'

def preview_html(url):
    if url:
        return '<a href="'+ url + '" >Listen on Spotify</a>'
    else:
        return None

records = []
for index, track in enumerate(recommendations['tracks']): 
    record = {
        "index": index,
        "name": track['name'],
        "artist": track["artists"][0]["name"],
        "popularity": track["popularity"],
        "preview_url": preview_html(track["preview_url"]),
        "album_art": img_html(track["album"]["images"][0]["url"])
    }
    records.append(record)

tracks_df = DataFrame(records)
tracks_df.head()

# displaying the dataframe as HTML, with HTML links and images:
tracks_table = HTML(tracks_df.to_html(escape=False, index=False, formatters=dict(Icon=img_html)))