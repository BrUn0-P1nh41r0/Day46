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
                            scope="user-library-read")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = "https://www.billboard.com/charts/hot-100/" + date

sp = spotipy.Spotify(auth_manager=AUTH_MANAGER)

response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")
soup_title = soup.select("li ul li h3")
song_names = []

for song in soup_title:
    song_names.append(song.getText().strip())

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

user = sp.user("11178817830")
print(user)