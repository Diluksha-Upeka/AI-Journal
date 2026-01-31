import cv2
import time
import os
import json
import re
import google.genai
import pyttsx3
from google.genai.errors import APIError
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

# Initialize the voice engine
try:
    # On Windows, SAPI5 is the most reliable backend.
    engine = pyttsx3.init(driverName="sapi5")
except Exception:
    engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate
engine.setProperty('volume', 1.0)


def _extract_json_object(text: str) -> str:
    """Best-effort extraction of a JSON object from model output."""
    cleaned = text.strip()

    # Remove markdown code fences if present
    if "```" in cleaned:
        if "```json" in cleaned:
            start = cleaned.find("```json") + 7
            end = cleaned.find("```", start)
            cleaned = cleaned[start:end].strip()
        else:
            start = cleaned.find("```") + 3
            end = cleaned.find("```", start)
            cleaned = cleaned[start:end].strip()

    # If the model wrapped extra prose around JSON, grab the first {...} block.
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last != -1 and last > first:
        cleaned = cleaned[first:last + 1]

    # Remove common "trailing comma" issues: {"a": 1,}
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    return cleaned

def speak_warning(text):
    """The Agentic Action: Speaking to the real world"""
    print(f"[Voice Alert]: {text}")
    try:
        engine.say(text)        # Queue the text to be spoken
        engine.runAndWait()     # runAndWait() blocks execution until speech is complete
    except Exception as e:
        print(f"[Voice Error] {type(e).__name__}: {e}")


# Log events to a file 
def log_event(report_text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("security_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(report_text.strip())
        f.write("\n" + "-"*50 + "\n")


# Main surveillance loop
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
    
    last_alert = ""  # Track last spoken alert to avoid repeating

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
Analyze this security camera feed as a security system.

Return ONLY a single, strict JSON object (no markdown fences, no commentary, no trailing commas) with exactly these keys:
{
  "activity": "what is happening",
  "threat_level": "Low" | "Medium" | "High",
  "alert_required": "A short, urgent spoken warning message. ALWAYS provide a warning for ANY activity detected (even Low threat). Examples: 'Unauthorized person detected', 'Movement in restricted area', 'Unknown individual approaching'. Only use 'No alert' if the frame is completely empty with zero activity."
}
            """.strip()

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, img]
                )

                response_text = _extract_json_object(response.text)

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
                
                # Trigger voice alert if needed
                try:
                    analysis = json.loads(response_text)
                    alert_msg = (analysis.get("alert_required") or "").strip()  # Get alert message
                    print(f"[DEBUG] Alert message: '{alert_msg}'")
                    if alert_msg and alert_msg.lower() != "no alert":
                        # Only speak if it's a different alert than last time
                        if alert_msg != last_alert:
                            print(f"[DEBUG] Triggering voice for: {alert_msg}")
                            speak_warning(alert_msg)
                            last_alert = alert_msg
                        else:
                            print("[DEBUG] Skipping voice (same alert as previous)")
                    else:
                        print("[DEBUG] No voice triggered (alert is 'No alert' or empty)")
                        last_alert = ""  # Reset when no alert
                except json.JSONDecodeError:
                    print("[Warning] Could not parse JSON response for voice alert")
            
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
