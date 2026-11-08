import os
import certifi
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Literal
from pydantic import BaseModel, Field
from PIL import Image
import json

# Force Python to find security certificates on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load variables from the .env file automatically
load_dotenv()

# Initialize the client (picks up GEMINI_API_KEY from the environment)
client = genai.Client()

class PictureAnalysis(BaseModel):
    birdorplane: Literal["bird", "aircraft", "other"] = Field(
        description="Classify whether the primary object in the image is a bird, aircraft, or neither"
    )

img = Image.open("../85825096-plane-in-the-sky-shooted-from-the-ground.jpg")

print("Sending request to Gemini API...")
response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents=[
        img, 
        "Classify whether the primary object in the image is a bird, aircraft, or neither"
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PictureAnalysis,
    )
)

data = json.loads(response)
result = data["birdorplane"]
print("\n--- Response ---")
print(response.text)