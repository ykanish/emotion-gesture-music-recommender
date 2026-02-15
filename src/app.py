import cv2
import time

from emotion.predict import predict_emotion
from emotion.utils import emotion_to_mood

from spotify.player import play_song_by_mood


def main():
    cap = cv2.VideoCapture(0)
    last_play_time = 0
    PLAY_COOLDOWN = 20

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        emotion = predict_emotion(frame)
        mood = emotion_to_mood(emotion)

        # ---- Spotify trigger with cooldown ----

        current_time = time.time()
        if current_time - last_play_time > PLAY_COOLDOWN:
            try:
                play_song_by_mood(mood)
                last_play_time = current_time
            except Exception as e:
                print(f"Error playing music: {e}")

        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Mood: {mood}",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv2.imshow("Emotion Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
