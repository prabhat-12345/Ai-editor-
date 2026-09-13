import streamlit as st
import requests
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Ultimate AI Studio", layout="wide")
st.title("🔥 FLUX AI Photo Studio")
st.write("Type your commands below to generate or edit high-definition visuals.")

# 2. Loading Secret API Key Safely from Streamlit Cloud Secrets
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except Exception:
    st.error("🚨 Configuration Missing: Please add 'HF_API_KEY' in your Streamlit Cloud Settings -> Secrets!")
    st.stop()

# Using Black Forest Labs FLUX.1-schnell model
MODEL_URL = "https://huggingface.co"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# 3. Layout Setup
col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ Enter Your Vision")
    
    # Detailed Prompt Input
    prompt = st.text_area(
        "Describe what you want to create in detail:", 
        placeholder="e.g., 'A stunning realistic portrait of a warrior, neon lighting, highly detailed, 4k resolution'",
        height=120
    )
    
    # Optional image upload
    uploaded_file = st.file_uploader("Optional: Upload a base image for context", type=["png", "jpg", "jpeg"])
    
    generate_btn = st.button("🚀 Generate High-End AI Image")

with col2:
    st.subheader("✨ AI Masterpiece Output")
    
    if generate_btn and prompt:
        with st.spinner("🎨 FLUX AI is rendering your masterpiece... (Takes 10-25 seconds)"):
            try:
                # Payload for FLUX Model
                payload = {
                    "inputs": prompt,
                    "parameters": {"width": 1024, "height": 1024, "num_inference_steps": 4}
                }
                
                response = requests.post(MODEL_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image_data = response.content
                    output_image = Image.open(io.BytesIO(image_data))
                    
                    # Display the final generated image
                    st.image(output_image, use_container_width=True, caption="Generated via FLUX")
                    
                    # Clean Download Button
                    st.download_button(
                        label="📥 Download HD Image",
                        data=image_data,
                        file_name="flux_output.png",
                        mime="image/png"
                    )
                elif response.status_code == 503:
                    st.warning("⏳ AI Model is warming up on the free server. Please wait 15 seconds and click 'Generate' again.")
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                    st.info("💡 Make sure your Hugging Face token is valid and has 'Read' access.")
                    
            except Exception as e:
                st.error(f"Network error: {e}")
    elif generate_btn and not prompt:
        st.warning("⚠️ Please write a detailed prompt instruction first!")
        
