from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS for frontend communication
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load trained model
model = tf.keras.models.load_model('deepfake_detector.h5')

def preprocess_image(image):
    try:
        image = image.convert("RGB")  # Ensure image is in RGB mode
        image = image.resize((128, 128))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        return image, None
    except Exception as e:
        return None, str(e)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        image = Image.open(file)
        processed_image, error = preprocess_image(image)
        if processed_image is None:
            return jsonify({"error": f"Image processing failed: {error}"}), 400

        prediction = model.predict(processed_image)[0][0]

        # Update logic: invert confidence if Deepfake
        if prediction > 0.5:
            label = "Real"
            confidence = round(prediction * 100, 2)
        else:
            label = "Deepfake"
            confidence = round((1 - prediction) * 100, 2)

        return jsonify({
            "label": label,
            "confidence": confidence,
            "message": f"The model is {confidence:.2f}% confident that this image is {label}."
        })

    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
