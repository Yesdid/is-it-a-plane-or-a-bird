import os
import sys
import certifi
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Literal
from pydantic import BaseModel, Field
from PIL import Image
import json
from google.genai.errors import ServerError
from flask import Flask, request, jsonify
from flask_cors import CORS

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from openskyPlane import get_nearby_aircraft
from bird_classifier import analyze_image

# GETTING IMAGE FROM FRONTEND

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '' or file is None:
        return jsonify({'error': 'No selected file'}), 400

    try:
        with Image.open(file.stream) as uploaded_image:
            img = uploaded_image.convert("RGB")
    except OSError:
        return jsonify({"error": "Uploaded file is not a valid image"}), 400

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            img,
            "Classify whether the primary object in the image is a bird, aircraft, or neither"
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PictureAnalysis,
        ),
    )

    if response.parsed is None:
        return jsonify({"error": "Gemini did not return a valid classification"}), 502

    label = response.parsed.birdorplane

    # Only search for nearby aircraft if Gemini identifies an aircraft
    if label == "aircraft":
        nearby_flights = get_nearby_aircraft()

        return jsonify({
            "birdorplane": label,
            "nearby_aircraft": nearby_flights
        }), 200

    if label == "bird":
        bird_predictions = analyze_image(img)

        return jsonify({
            "birdorplane": label,
            "bird_predictions": bird_predictions
        }), 200

    return jsonify({
        "birdorplane": "other",
        "message": "The image does not appear to show a bird or aircraft."
    }), 200


# Force Python to find security certificates on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()

# Find the absolute path to the .env file up one directory level
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path, override=True)

# Verify the key actually loaded before hitting the network
if not os.environ.get("GEMINI_API_KEY"):
    print("ERROR: GEMINI_API_KEY is empty or missing from your .env file!")
    print(f"Looked for .env at: {dotenv_path}")
    exit(1)

# Initialize the client securely
client = genai.Client()

class PictureAnalysis(BaseModel):
    birdorplane: Literal["bird", "aircraft", "other"] = Field(
        description="Classify whether the primary object in the image is a bird, aircraft, or neither"
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)