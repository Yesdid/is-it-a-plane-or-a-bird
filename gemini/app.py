import os
import certifi
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# Force Python to find security certificates on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()

# Find the absolute path to the .env file up one directory level
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

# Verify the key actually loaded before hitting the network
if not os.environ.get("GEMINI_API_KEY"):
    print("ERROR: GEMINI_API_KEY is empty or missing from your .env file!")
    print(f"Looked for .env at: {dotenv_path}")
    exit(1)

# Initialize the client securely
client = genai.Client()

print("Sending request to Gemini API...")

# Try the request with a built-in safety net for 503 high demand spikes
for attempt in range(3):
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents='Write a haiku about coding with AI.',
        )
        print("\n--- Response ---")
        print(response.text)
        break # Exit loop immediately on success
    except ServerError as e:
        if "503" in str(e) and attempt < 2:
            print(f"Server busy (503). Retrying in 2 seconds... (Attempt {attempt + 1}/3)")
            time.sleep(2)
        else:
            print(f"Gemini Server Error: {e}")
            break
    except Exception as e:
        print(f"Unexpected Error: {e}")
        break
