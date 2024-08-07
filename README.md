# Spotify-Song-Recommender

## Setup
Create virtual environment:
```sh
conda create -n spotify-env python=3.11
conda activate spotify-flask
conda create -n spotify-flask python=3.10
```

Activate the environment: 
```sh
conda activate spotify-env 
```
Install Packages:
```sh
pip install -r requirements.txt
```

## Usage

Run the script:
```sh
python -m app.songrecommender 
```
Run the web app (then view in the browser at http://localhost:5000/):
```sh
FLASK_APP="web_app" flask run
```

```sh
# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing
Run Tests:
```sh
pytest
```

### Credentials

Login to the Spotify Developer console, create a new app, set redirect url of "http://localhost:5000/auth/spotify/callback". Note the app's client id and client secret. Provide these credentials via ".env" file approach (see below).
