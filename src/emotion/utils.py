def emotion_to_mood(emotion: str) -> str:
    """
    Maps detected emotion to a music mood.
    """

    emotion = emotion.lower()

    mapping = {
        "happy": "party",
        "sad": "acoustic",
        "angry": "rock",
        "neutral": "chill",
        "fear": "ambient",
        "surprise": "pop",
    }

    return mapping.get(emotion, "chill")
