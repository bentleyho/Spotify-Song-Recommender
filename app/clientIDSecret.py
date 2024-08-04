import os
from dotenv import load_dotenv

#ENVIRONMENT VARIABLE RELATED CODE:

load_dotenv() # look in the env file for env vars

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")