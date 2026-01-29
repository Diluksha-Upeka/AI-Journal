import streamlit as st
import time
import json
import os
from PIL import Image

st.set_page_config(page_title="Surveillance Dashboard", layout="wide", page_icon="🛡️")

# CSS for Modern Security Dashboard UI
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background-color: #0F1116;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    h1 {
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
        font-weight: 600;
        font-size: 2rem;
        letter-spacing: -0.5px;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #2D3748;
    }

    /* Cards */
    div[data-testid="stColumn"] {
        background-color: #1A202C;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2D3748;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Captions/Labels */
    div[data-testid="stCaptionContainer"] {
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }

    /* Alerts and Info Boxes */
    .stAlert {
        border-radius: 8px;
        border: none;
        background-color: #2D3748;
        color: #E2E8F0;
    }
    
    /* Code block for objects */
    code {
        color: #63B3ED;
        background-color: #171923;
        border: 1px solid #2D3748;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Surveillance Dashboard")

# Placeholders for live updates
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.caption("LIVE SURVEILLANCE FEED")
    img_placeholder = st.empty()

with col2:
    st.caption("REAL-TIME ANALYSIS")
    data_placeholder = st.empty()



while True:
    # Check if the current view image exists
    if os.path.exists("current_view.jpg"):
        try:
            # Load and display the image with retry
            for attempt in range(3):
                try:
                    img = Image.open("current_view.jpg")
                    img_placeholder.image(img, caption="Live Feed", use_container_width=True)
                    break
                except (IOError, OSError) as e:
                    if attempt < 2:
                        time.sleep(0.1)  # Wait 100ms before retry
                    else:
                        img_placeholder.error(f"Failed to load image after 3 attempts")
        except Exception as e:
            img_placeholder.error(f"Image error: {type(e).__name__}")

    # Check if the latest scan JSON exists
    if os.path.exists("latest_scan.json"):
        data = None
        for attempt in range(3):
            try:
                # Load and display the JSON data with retry
                with open("latest_scan.json", "r") as f:
                    content = f.read()
                
                # Skip if file is empty (being written)
                if not content.strip():
                    if attempt < 2:
                        time.sleep(0.1)
                        continue
                    else:
                        break
                    
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    start = content.find("```json") + 7
                    end = content.find("```", start)
                    content = content[start:end].strip()
                elif "```" in content:
                    start = content.find("```") + 3
                    end = content.find("```", start)
                    content = content[start:end].strip()
                    
                data = json.loads(content)
                break  # Success!
                    
            except (json.JSONDecodeError, IOError, OSError) as e:
                if attempt < 2:
                    time.sleep(0.1)  # Wait 100ms before retry
                else:
                    data_placeholder.error(f"JSON Parse Error: {type(e).__name__}")
            except Exception as e:
                data_placeholder.error(f"Unexpected error: {str(e)}")
                break
        
        # Display data if successfully loaded
        if data:
            try:
                with data_placeholder.container():
                    # 1. Threat Level (Prominent Header)
                    threat_level = data.get("threat_level", "Unknown")
                    if threat_level == "Low":
                        st.success(f"THREAT LEVEL: {threat_level.upper()}")
                    else:
                        st.error(f"THREAT LEVEL: {threat_level.upper()}")
                    
                    # 2. Activity Analysis (Easy to read, large font)
                    st.markdown("### Activity Analysis")
                    st.info(data.get('activity'), icon="ℹ️")

                    # 3. Detected Objects (Compact, small text)
                    st.markdown("####  Objects Detected")
                    objects = data.get("detected_objects", [])
                    if objects:
                        # Display as pills or compact string to save space
                        st.code(", ".join(objects), language="text")
                    else:
                        st.caption("No objects detected in current frame.")
                    
                    # 4. Critical Alert
                    if data.get("alert_required"):
                        st.error("SECURITY ALERT: IMMEDIATE ATTENTION REQUIRED")
                    
                    # Timestamp
                    try:
                        mtime = os.path.getmtime('latest_scan.json')
                        st.caption(f"Last Scan: {time.strftime('%H:%M:%S', time.localtime(mtime))}")
                    except:
                        pass
            except Exception as e:
                data_placeholder.error(f"Display error: {str(e)}")

    # Refresh every 2 seconds (less aggressive than 1 sec, reduces CPU/flickering)
    time.sleep(2)
    st.rerun()