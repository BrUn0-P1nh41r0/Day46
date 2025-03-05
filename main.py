from pprint import pprint
import requests
import os
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SPO_CLIENT_ID = os.environ["SPO_CLIENT_ID"]
SPO_CLIENT_SECRET = os.environ["SPO_CLIENT_SECRET"]
SPO_REDIRECT_URL = os.environ["SPO_REDIRECT_URL"]

AUTH_MANAGER = SpotifyOAuth(client_id=SPO_CLIENT_ID,
                            client_secret=SPO_CLIENT_SECRET,
                            redirect_uri=SPO_REDIRECT_URL,
                            scope="playlist-modify-private",
                            show_dialog=True,
                            cache_path=".cache")

sp = spotipy.Spotify(auth_manager=AUTH_MANAGER)

user_id = sp.current_user()["id"]
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")
soup_title = soup.select("li ul li h3")
song_names = []
song_uri = []

for song in soup_title:
    song_names.append(song.getText().strip())

year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
