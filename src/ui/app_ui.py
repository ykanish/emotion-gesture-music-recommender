import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import cv2
import time

from emotion.predict import predict_emotion
from emotion.utils import emotion_to_mood
from spotify.player import play_song_by_mood

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Emotion Music Recommender",
    layout="centered"
)

st.title("🎵 Emotion-Based Music Recommender")
st.caption("Real-time facial emotion detection + Spotify playback")

st.markdown("---")

# ----------------------------------
# Controls
# ----------------------------------
start = st.checkbox("▶️ Start Camera")

col1, col2 = st.columns(2)

with col1:
    lock_mood = st.checkbox("🔒 Lock Mood")

with col2:
    manual_mood = st.selectbox(
        "🎚 Manual Override",
        ["Auto", "chill", "party", "rock", "acoustic", "pop", "ambient", "metal"]
    )

st.markdown("---")

# ----------------------------------
# UI Placeholders
# ----------------------------------
frame_placeholder = st.image([])
status_placeholder = st.empty()
play_status_placeholder = st.empty()

PLAY_COOLDOWN = 20

# ----------------------------------
# Main Logic
# ----------------------------------
if start:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Unable to access camera")
    else:
        last_play_time = 0
        current_locked_mood = None

        while start:
            ret, frame = cap.read()
            if not ret:
                st.warning("Camera read failed")
                break

            emotion = predict_emotion(frame)
            mood = emotion_to_mood(emotion)

            # Manual override
            if manual_mood != "Auto":
                mood = manual_mood

            # Lock mood
            if lock_mood:
                if current_locked_mood is None:
                    current_locked_mood = mood
                mood = current_locked_mood
            else:
                current_locked_mood = None

            # Spotify trigger with cooldown
            current_time = time.time()
            if current_time - last_play_time > PLAY_COOLDOWN:
                try:
                    play_song_by_mood(mood)
                    play_status_placeholder.success(f"🎶 Playing: {mood} mood")
                    last_play_time = current_time
                except Exception as e:
                    play_status_placeholder.error("Spotify playback error")

            # Update UI
            status_placeholder.markdown(
                f"""
                ### 🧠 Emotion: `{emotion}`
                ### 🎧 Mood: `{mood}`
                """
            )

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb)

        cap.release()

else:
    st.info("Enable 'Start Camera' to begin the demo")
