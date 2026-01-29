import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

IMG_SIZE = 224
MODEL_PATH = "models/garbage_classifier.h5"

CLASS_NAMES = ['empty', 'full', 'half', 'overflow']

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    idx = np.argmax(preds)
    
    return {
        "label": CLASS_NAMES[idx],
        "confidence": float(preds[0][idx]) * 100
    }
