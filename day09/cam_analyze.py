import cv2
import time
import os
import google.genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

def analyze_image():
    # Open the webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Taking the picture in 3 seconds...")
    time.sleep(3)  # Wait for 3 seconds before taking the picture

    # Capture a single frame
    ret, frame = cap.read() # Read a frame from the webcam

    # Save it temporarily
    cv2.imwrite("captured_image.jpg", frame)

    # Release the webcam
    cap.release()           # Release the webcam
    cv2.destroyAllWindows() # Close any OpenCV windows

    print("Image captured. Analyzing...")

    # GEMINI ANALYSIS
    img_path = "captured_image.jpg"
    img = Image.open(img_path)

    # Prompt for analysis
    prompt = (
        "You are a high-end fashion designer. Roast the outfit of the person in this image. Be mean."
    )

    response = client.models.generate_content(
        model = model_name,
        contents = [prompt,img]
    )

    # Print the analysis
    print("\n--- Analysis Result ---")
    print(response.text)
    print("-----------------------\n")

# Cleanup
    os.remove(img_path) # Uncomment to delete the file after

if __name__ == "__main__":  
    analyze_image()