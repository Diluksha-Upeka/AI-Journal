
# AI Journal — Day 10 Surveillance App

A lightweight “security camera” demo that:

- Captures frames from a webcam (or an optional video file)
- Sends a frame to Google Gemini for scene/security analysis
- Writes the latest analysis to a JSON file for a Streamlit dashboard
- Speaks an audible warning when an alert is present

This folder contains two main entry points:

- `security_loop.py` — the continuous capture + analysis + voice-alert loop
- `dashboard.py` — a Streamlit UI that displays the live frame + JSON analysis

---

## Features

### Continuous analysis loop
- Captures a frame every ~5 seconds.
- Uses Gemini to return a strict JSON object describing activity + threat level + an alert message.
- Writes outputs using atomic file replacement (prevents the dashboard from reading partial files).

### Dashboard UI (Streamlit)
- Shows the latest frame (`current_view.jpg`).
- Shows the latest JSON analysis (`latest_scan.json`).
- Highlights threat level and the alert message.
- Optional browser-based voice alert (uses `speechSynthesis` in your browser).

### Voice alerts (two layers)
You can get voice alerts in two different ways:

1) **Python TTS (pyttsx3)**: `security_loop.py` speaks alerts through Windows TTS.
2) **Browser TTS**: `dashboard.py` speaks alerts via the browser (when a *new* alert appears).

---

## Project layout (Day 10)

- `day10/security_loop.py` — capture + analyze + write JSON/image + speak alerts
- `day10/dashboard.py` — Streamlit dashboard

The loop also creates/updates these files in the project root (same folder you run from):

- `current_view.jpg` — most recent captured frame
- `latest_scan.json` — most recent model output (JSON)
- `security_log.txt` — append-only log of all analyses

---

## Prerequisites

- Windows (recommended for the current `pyttsx3` configuration)
- Python 3.10+ (tested locally with Python 3.12)
- A webcam (if you don’t provide a video file)
- A Google Gemini API key

---

## Setup

### 1) Create and activate a virtual environment

From the repo root:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

The repo root `requirements.txt` covers Streamlit + dotenv + OpenCV. Day 10 also needs Gemini + Pillow + TTS.

```powershell
python -m pip install -r requirements.txt
python -m pip install google-genai pillow pyttsx3
```

If you want to pin everything into `requirements.txt` later, you can add:

- `google-genai`
- `pillow`
- `pyttsx3`

### 3) Create a `.env` file

Create a `.env` file in the repo root (same level as `requirements.txt`) with:

```env
GOOGLE_API_KEY=your_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Notes:
- `GOOGLE_GEMINI_MODEL` is optional (defaults to `gemini-2.5-flash`).
- Keep your API key private.

---

## Running the app

You typically run **two processes** in two terminals.

### Terminal 1 — start the surveillance loop

From the repo root:

```powershell
python day10\security_loop.py
```

What you should see:
- A message about webcam vs video file
- “Analyzing the current view…” every cycle
- A printed JSON report
- Debug lines like `[DEBUG] Alert message: '...'`

### Terminal 2 — start the dashboard

From the repo root:

```powershell
streamlit run day10\dashboard.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

---

## Video source options

By default, the loop tries a local file named `sample_video.mp4`:

- If `sample_video.mp4` exists (in the repo root), it will be used.
- Otherwise, it falls back to the webcam (`cv2.VideoCapture(0)`).

To use a video file:
1) Put `sample_video.mp4` in the repo root
2) Re-run `python day10\security_loop.py`

---

## Output JSON schema

The loop asks Gemini to output a strict JSON object:

```json
{
	"activity": "what is happening",
	"threat_level": "Low" | "Medium" | "High",
	"alert_required": "..." | "No alert"
}
```

`dashboard.py` also tries to display `detected_objects` if present, but `security_loop.py` does not currently ask Gemini for it. If you want object lists on the UI, update the prompt in `security_loop.py` to include a `detected_objects` array.

---

## Voice alerts (how they work)

### Python voice (from `security_loop.py`)

- Trigger condition: `alert_required` is a non-empty string and not `"No alert"`.
- Dedup: it won’t repeat the *same* alert message twice in a row.
- Engine: `pyttsx3` (Windows SAPI5).

If you get no sound:
- Make sure Windows volume isn’t muted.
- Make sure the terminal is actually printing `[DEBUG] Triggering voice for: ...`.

### Browser voice (from `dashboard.py`)

- Trigger condition: a new alert is displayed and it’s different from the previous alert.
- Uses the browser’s `speechSynthesis`.
- This depends on browser permissions/autoplay rules.

---

