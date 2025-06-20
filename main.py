# Install required packages
from flask import Flask, redirect, request, session, jsonify, render_template
import requests
import os
import base64
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Setup the flask server
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Get environment secrets
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

@app.route("/")
def login():
    auth_query = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "client_id": CLIENT_ID,
    }
    query_string = "&".join([f"{k}={requests.utils.quote(v)}" for k, v in auth_query.items()])
    return redirect(f"{AUTH_URL}?{query_string}")

@app.route("/callback")
def callback():
    code = request.args.get("code")

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    res = requests.post(TOKEN_URL, headers=headers, data=data)
    res_data = json.loads(res.content)

    session["access_token"] = res_data["access_token"]
    return redirect("/currently-playing")

@app.route("/currently-playing")
def currently_playing():
    access_token = session.get("access_token")
    if not access_token:
        return redirect("/")

    song = get_np(access_token=access_token)
    return render_template("currently_playing.html", song=song.dumps())

class Song:
    playing: bool = False
    artist: str = ""
    name: str = ""
    url: str = ""
    id_: str = ""
    progress_ms: int = 0
    duration_ms: int = 0
    bpm: int = 0

    def __init__(self, content: str):
        try:
            song = json.loads(content)
            item = song['item']
            song_artists = [artist['name'] for artist in item['album']['artists']]
            song_artist_fmt = ", ".join(song_artists)
            song_name = item['name']
            song_url = item['external_urls']['spotify']
            song_id = item['id']

            self.playing = True
            self.artist = song_artist_fmt
            self.name = song_name
            self.url = song_url
            self.id = song_id
            self.progress_ms = song['progress_ms']
            self.duration_ms = item['duration_ms']
            self.bpm = int(get_track_info(self.id))
        except:
            self.playing = False
            print("Not playing anything")

    def dumps(self):
        d = {
            "playing": self.playing
        }
        if self.playing:
            d = {
                "playing": self.playing,
                "artist": self.artist,
                "name": self.name,
                "url": self.url,
                "id": self.id_,
                "progress_ms": self.progress_ms,
                "duration_ms": self.duration_ms,
                "bpm": self.bpm,
            }
        return json.dumps(d)
        

def get_np(access_token) -> Song:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    res = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    return Song(res.content)

def get_track_info(song_id):
    res = requests.get(f"https://songdata.io/track/{song_id}")
    soup = BeautifulSoup(res.content, "html.parser")
    bpm = soup.find("dd")
    return bpm.text if bpm else "N/A"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
