import streamlit as st
import requests
from PIL import Image
import io

# Page Configuration
st.set_page_config(page_title="🌟 Ultimate AI Photo Creator & Editor", layout="wide")
st.title("🔥 FLUX-Powered AI Studio (ChatGPT/DALL-E Style)")
st.write("Type your creative commands below and let the state-of-the-art FLUX model build high-definition visuals.")

# Using Black Forest Labs FLUX.1-schnell (Incredible photorealism and prompt adherence)
MODEL_URL = "https://huggingface.co"

# Enter your Free Hugging Face Token here
HF_API_KEY = "YOUR_HUGGINGFACE_API_KEY_HERE"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Layout Setup
col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ Enter Your Vision")
    # Prompt input for high-end generation/editing instruction
    prompt = st.text_area(
        "Describe what you want to create or modify in extreme detail:", 
        placeholder="e.g., 'A hyper-realistic cinematic portrait of a cyberpunk samurai in Tokyo rain, neon lights, 8k resolution, photorealistic'",
        height=120
    )
    
    # Optional reference image upload for context
    uploaded_file = st.file_uploader("Optional: Upload a base image for reference", type=["png", "jpg", "jpeg"])
    
    generate_btn = st.button("🚀 Generate High-End AI Image")

with col2:
    st.subheader("✨ FLUX Masterpiece Output")
    
    if generate_btn and prompt:
        if HF_API_KEY == "YOUR_HUGGINGFACE_API_KEY_HERE" or not HF_API_KEY:
            st.error("🚨 Please paste your valid Hugging Face API key inside the `app.py` file code!")
        else:
            with st.spinner("🎨 FLUX AI is rendering your masterpiece... (Takes 10-25 seconds)"):
                try:
                    # Preparing payload
                    payload = {
                        "inputs": prompt,
                        "parameters": {"width": 1024, "height": 1024, "num_inference_steps": 4}
                    }
                    
                    response = requests.post(MODEL_URL, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        image_data = response.content
                        output_image = Image.open(io.BytesIO(image_data))
                        
                        st.image(output_image, use_container_width=True, caption="Generated via FLUX.1-schnell")
                        
                        # Download Button
                        st.download_button(
                            label="📥 Download HD Image",
                            data=image_data,
                            file_name="flux_masterpiece.png",
                            mime="image/png"
                        )
                    elif response.status_code == 503:
                        st.warning("⏳ AI Model is warming up on the free server. Please wait 15 seconds and click 'Generate' again.")
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                        
                except Exception as e:
                    st.error(f"Network or processing error: {e}")
    elif generate_btn and not prompt:
        st.warning("⚠️ Please write a detailed prompt instruction first!")
      
