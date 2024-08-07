# web_app/__init__.py

from flask import Flask
from web_app.routes.spotify_routes import spotify_routes
from web_app.routes.home_routes import home_routes
import os
import logging

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Register blueprints
    app.register_blueprint(spotify_routes)
    app.register_blueprint(home_routes)

    return app
