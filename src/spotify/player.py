from spotify.client import get_spotify_client
import random

# In-memory history (resets when app restarts)
played_tracks_by_mood = {}

MAX_HISTORY_PER_MOOD = 5   # keep it small for demo

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

    # Search for multiple tracks
    results = sp.search(q=query, type="track", limit=10)
    tracks = results["tracks"]["items"]

    if not tracks:
        return

    # Initialize history for mood
    if mood not in played_tracks_by_mood:
        played_tracks_by_mood[mood] = []

    played_uris = played_tracks_by_mood[mood]

    # Filter out already played tracks
    fresh_tracks = [
        track for track in tracks
        if track["uri"] not in played_uris
    ]

    # If all tracks exhausted → reset history
    if not fresh_tracks:
        played_tracks_by_mood[mood] = []
        fresh_tracks = tracks

    # Pick a random fresh track
    selected_track = random.choice(fresh_tracks)
    track_uri = selected_track["uri"]

    # Play track
    sp.start_playback(uris=[track_uri])

    # Update history
    played_tracks_by_mood[mood].append(track_uri)

    # Keep history bounded
    if len(played_tracks_by_mood[mood]) > MAX_HISTORY_PER_MOOD:
        played_tracks_by_mood[mood].pop(0)

    print(f"Playing {selected_track['name']} by {selected_track['artists'][0]['name']}")