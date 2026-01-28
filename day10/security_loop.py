import cv2
import time
import os
import google.genai
from google.genai.errors import APIError
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

def start_surveillance():
    cap = cv2.VideoCapture(0)

    print("Security surveillance started. Press 'Ctrl+C' to stop.")
    print("Monitoring frequency: Every 5 seconds.")

    try:
        while True:
            # Capture a single frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not capture frame.")
                break

            # Save temporary image
            cv2.imwrite("current_view.jpg", frame)

            # Analyze the image using Gemini
            print("Analyzing the current view...")
            img = Image.open("current_view.jpg")

            # Structure the prompt for analysis
            prompt = """
            Analyze this security camera feed. Return a valid JSON object with:
            {
                "detected_objects": [list of visible items/people],
                "activity": "what is happening",
                "threat_level": "Low/Medium/High",
                "alert_required": true/false
            }
            """

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, img]
                )

                # Print the analysis
                print("\n--- Surveillance Analysis ---")
                print(response.text)
                print("------------------------------\n")
            
            except APIError as e:
                # Handle API errors gracefully (503, rate limits, etc.)
                print(f"\n[API Error] {e.status_code}: {e.message}")
                print("Skipping this frame and continuing surveillance...\n")
            except Exception as e:
                # Handle any other unexpected errors
                print(f"\n[Unexpected Error] {type(e).__name__}: {str(e)}")
                print("Skipping this frame and continuing surveillance...\n")

            # Cleanup
            # Wait for 5 seconds before the next capture
            time.sleep(5)

    except KeyboardInterrupt:
        print("Surveillance stopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    start_surveillance()
