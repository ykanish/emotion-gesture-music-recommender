from emotion.predict import predict_emotion

def main():
    emotion = predict_emotion(None)
    print(f"Detected emotion: {emotion}")

if __name__ == "__main__":
    main()
