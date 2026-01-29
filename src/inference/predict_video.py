import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

MODEL_PATH = "models/garbage_classifier.h5"
IMG_SIZE = 224

model = load_model(MODEL_PATH)

# Mapping class indices to labels
CLASS_MAP = {0: "empty", 1: "full", 2: "half", 3: "overflow"}

def predict_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_predictions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and preprocess frame
        frame_resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        frame_array = img_to_array(frame_resized) / 255.0
        frame_array = np.expand_dims(frame_array, axis=0)

        # Predict frame
        preds = model.predict(frame_array)
        label_index = np.argmax(preds)
        frame_predictions.append(label_index)

    cap.release()

    # Aggregate predictions across frames
    counts = np.bincount(frame_predictions, minlength=len(CLASS_MAP))
    majority_index = np.argmax(counts)
    confidence = counts[majority_index] / len(frame_predictions) * 100

    label = CLASS_MAP[majority_index]
    return {"label": label, "confidence": round(confidence, 2)}
