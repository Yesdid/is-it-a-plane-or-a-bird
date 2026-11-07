import os
import certifi
from dotenv import load_dotenv
from google import genai

# Force Python to find security certificates on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load variables from the .env file automatically
load_dotenv()

# Initialize the client (picks up GEMINI_API_KEY from the environment)
client = genai.Client()

print("Sending request to Gemini API...")
response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents='Write a haiku about coding with AI.',
)

print("\n--- Response ---")
print(response.text)