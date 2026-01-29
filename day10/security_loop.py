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

def log_event(report_text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("security_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(report_text.strip())
        f.write("\n" + "-"*50 + "\n")


def start_surveillance():
    video_source = "sample_video.mp4"
    if os.path.exists(video_source):
        cap = cv2.VideoCapture(video_source)
        print(f"Using video file: {video_source}")
    else:
        cap = cv2.VideoCapture(0)
        print("Sample video not found. Using webcam.")

    print("Security surveillance started. Press 'Ctrl+C' to stop.")
    print("Monitoring frequency: Every 5 seconds.")

    try:
        while True:
            # Capture a single frame
            ret, frame = cap.read()
            if not ret:
                # If using a file, loop back to start
                if os.path.exists(video_source):
                    print("Video ended, restarting loop...")
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
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

                # Extract JSON from response (remove markdown code blocks if present)
                response_text = response.text
                if "```json" in response_text:
                    start = response_text.find("```json") + 7
                    end = response_text.find("```", start)
                    response_text = response_text[start:end].strip()
                elif "```" in response_text:
                    start = response_text.find("```") + 3
                    end = response_text.find("```", start)
                    response_text = response_text[start:end].strip()

                # Save Data frontend will read this (atomic write)
                temp_json = "latest_scan.json.tmp"
                with open(temp_json, "w") as f:
                    f.write(response_text)
                os.replace(temp_json, "latest_scan.json")  # Atomic operation
                    
                # Copy the frame for dashboard display (atomic write)
                temp_img = "current_view.jpg.tmp"
                cv2.imwrite(temp_img, frame)
                os.replace(temp_img, "current_view.jpg")  # Atomic operation
                    
                # Print the analysis
                print("\n--- Surveillance Analysis ---")
                print(response_text)
                log_event(response_text)
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
