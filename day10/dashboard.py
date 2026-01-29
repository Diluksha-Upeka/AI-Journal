import streamlit as st
import time
import json
import os
from PIL import Image

st.set_page_config(layout="wide")
st.title("Security Surveillance Dashboard")

#Placeholders for live updates
col1, col2 = st.columns(2)
with col1:
    img_placeholder = st.empty()
with col2:
    data_placeholder = st.empty()

st.warning ("Ensure 'security_loop.py'  is running in a separate terminal")

while True:
    # Check if the current view image exists
    if os.path.exists("current_view.jpg"):
        try:
            # Load and display the image with retry
            for attempt in range(3):
                try:
                    img = Image.open("current_view.jpg")
                    img_placeholder.image(img, caption="Live Feed", use_column_width=True)
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
                    status_color = "green" if data.get("threat_level") == "Low" else "red"
                    st.markdown(f"### Threat Level: :{status_color}[{data.get('threat_level')}]")
                    
                    st.write("**Detected Objects:**")
                    for obj in data.get("detected_objects", []):
                        st.write(f"- {obj}")
                        
                    st.info(f"📝 Activity: {data.get('activity')}")
                    
                    if data.get("alert_required"):
                        st.warning("⚠️ Alert Required")
                    
                    try:
                        mtime = os.path.getmtime('latest_scan.json')
                        st.caption(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))}")
                    except:
                        st.caption("Last Updated: Unknown")
            except Exception as e:
                data_placeholder.error(f"Display error: {str(e)}")

    # Refresh every 2 seconds (less aggressive than 1 sec, reduces CPU/flickering)
    time.sleep(2)
    st.rerun()