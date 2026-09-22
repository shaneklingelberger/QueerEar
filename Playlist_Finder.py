import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import random
import time


# -----------------------------
# Spotify API credentials
# -----------------------------
CLIENT_ID = "INSERT YOUR OWN ID"
CLIENT_SECRET = "INSERT YOUR OWN SECRET"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
)


# -----------------------------
# Search terms
# -----------------------------
keywords = [
    "gay",
    "homosexual",
    "pride",
    "lgbt",
    "queer"
]


matching_playlists = {}
keyword_set = set(keywords)


# -----------------------------
# Search playlists
# -----------------------------
def search_playlists(keyword):
    playlists = []

    offset = 0

    while offset < 1000:  # Spotify max search depth
        results = sp.search(
            q=keyword,
            type="playlist",
            limit=10,
            offset=offset
        )

        items = results["playlists"]["items"]

        if not items:
            break

        playlists.extend(items)

        offset += 10

        time.sleep(0.1)

    return playlists


# -----------------------------
# Collect playlists
# -----------------------------
for word in keywords:
    print(f"Searching: {word}")

    results = search_playlists(word)

    for playlist in results:
        if playlist is None:
            continue

        name = playlist["name"]

        # Verify keyword is actually in title
        title_lower = name.lower()

        matching_playlists[playlist["id"]] = {
            "playlist_name": name,
            "playlist_id": playlist["id"],
            "owner": playlist["owner"]["display_name"],
            "url": playlist["external_urls"]["spotify"]
        }

all_playlists = list(matching_playlists.values())

print(f"Found {len(all_playlists)} matching playlists")

# -----------------------------
# Export CSV
# -----------------------------
df = pd.DataFrame(all_playlists)

df.to_csv(
    "queer_playlists.csv",
    index=False
)

print(
    f"Saved {len(all_playlists)} playlists to queer_playlists.csv"
)