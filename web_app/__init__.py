
# this is the "web_app/__init__.py" file...

import os
from dotenv import load_dotenv
from flask import Flask

from app.songrecommender import spotify_oauth
from web_app.routes.home_routes import home_routes
from web_app.routes.spotify_routes import spotify_routes

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret") # set this to something else on production!!!

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Register blueprints
    app.register_blueprint(spotify_routes)
    app.register_blueprint(home_routes)

    return app
