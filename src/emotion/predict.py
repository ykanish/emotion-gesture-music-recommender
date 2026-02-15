import cv2
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "models/emotion_model.h5"

EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

model = load_model(MODEL_PATH, compile=False)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def predict_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "neutral"

    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (64, 64))
    face = face / 255.0
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)

    preds = model.predict(face, verbose=0)
    return EMOTIONS[np.argmax(preds)]
