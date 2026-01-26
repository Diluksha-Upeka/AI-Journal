import os
from pathlib import Path
import io

from google import genai
from dotenv import load_dotenv
from google.genai import types
from PIL import Image

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

# Query the model with the image
response = client.models.generate_content(
    model=model_name,
    contents=[
        "Describe this image specifically for a blind person.",
        image_part
    ]
)

# OUTPUT
print(response.text)