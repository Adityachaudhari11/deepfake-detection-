from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__, static_folder="frontend/build")
CORS(app)  # Allow cross-origin requests

# Load trained model
model_path = "deepfake_detector.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")
model = tf.keras.models.load_model(model_path)

def preprocess_image(image):
    try:
        image = image.convert("RGB")  # Ensure RGB
        image = image.resize((128, 128))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        return image, None
    except Exception as e:
        return None, str(e)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    try:
        image = Image.open(file)
        processed_image, error = preprocess_image(image)
        if processed_image is None:
            return jsonify({"error": f"Image processing failed: {error}"}), 400

        prediction = model.predict(processed_image)[0][0]

        # Determine label
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

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
