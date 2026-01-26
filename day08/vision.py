import os
from pathlib import Path
import io

from google import genai
from dotenv import load_dotenv
from google.genai import types
from PIL import Image
import json

load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

# Load the image
image_path = Path("image.jpg")
if not image_path.exists():
    raise FileNotFoundError(f"Image file not found at {image_path}")

# Open and convert the image to bytes
img = Image.open(image_path)    # Open image using PIL/Pillow
buf = io.BytesIO()              # Create a bytes buffer(Like a virtual RAM) 
img.save(buf, format='JPEG')    # Save image to buffer in JPEG format
image_part = types.Part.from_bytes(
    data=buf.getvalue(),        # Extracts the raw bytes from buffer
    mime_type="image/jpeg")     # Specify MIME type (JPEG image)

# JSON prompt part
prompt = (
    "Analyze this image. Return a JSON object with keys: "
    "{'objects_detected': [], 'main_color': '', 'is_safe_for_work': true/false}."
)

# Query the model with the image
response = client.models.generate_content(
    model=model_name,
    contents=[
        prompt,
        image_part
    ]
)

json_string = response.text

try:
    data = json.loads(json_string)
except json.JSONDecodeError:
    print("Failed to parse JSON response")
    print("JSON string:", json_string)
    exit()

# OUTPUT
print("Objects Detected:", data.get('objects_detected', []))
print("Main Color:", data.get('main_color', ''))
print("Is Safe for Work:", data.get('is_safe_for_work', True))