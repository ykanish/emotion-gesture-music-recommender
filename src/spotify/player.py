from spotify.client import get_spotify_client

def play_song_by_mood(mood: str):
    sp = get_spotify_client()

    query_map = {
        "party": "party hits",
        "chill": "chill vibes",
        "acoustic": "acoustic",
        "rock": "rock",
        "pop": "pop",
        "ambient": "ambient",
        "metal": "metal",
    }

    query = query_map.get(mood, "chill vibes")

    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
