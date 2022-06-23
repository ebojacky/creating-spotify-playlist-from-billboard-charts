from pprint import pprint
import bs4
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

song_date = input("Enter date for top 100 songs on billboard (YYYY-MM-DD): ")
URL = f"https://www.billboard.com/charts/hot-100/{song_date}"
response = requests.get(URL)
soup = bs4.BeautifulSoup(response.text, "html.parser")
songs = [item.text.replace("\n", "").replace("\t", "")
        for item in soup.select("li ul li h3")]
print(songs)

key = "**************************"
secret = "*************************"
redirect_url = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=key,
        client_secret=secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = song_date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

pprint(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{song_date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
