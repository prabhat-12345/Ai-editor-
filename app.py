import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Ultimate AI Studio", layout="wide")
st.title("🔥 FLUX AI Photo Studio")
st.write("Type your commands below to generate high-definition visuals using official API methods.")

# 2. Loading Secret API Key Safely from Streamlit Cloud Secrets
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except Exception:
    st.error("🚨 Configuration Missing: Please add 'HF_API_KEY' in your Streamlit Cloud Settings -> Secrets!")
    st.stop()

# Using Official Hugging Face Client to bypass CloudFront 403 errors
@st.cache_resource
def get_ai_client(api_key):
    return InferenceClient(model="black-forest-labs/FLUX.1-schnell", token=api_key)

client = get_ai_client(HF_API_KEY)

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
    
    generate_btn = st.button("🚀 Generate High-End AI Image")

with col2:
    st.subheader("✨ AI Masterpiece Output")
    
    if generate_btn and prompt:
        with st.spinner("🎨 FLUX AI is rendering your masterpiece... (Takes 10-25 seconds)"):
            try:
                # Utilizing the official text_to_image method from the library
                output_image = client.text_to_image(prompt)
                
                # Display the final generated image
                st.image(output_image, use_container_width=True, caption="Generated via FLUX Official Client")
                
                # Convert image to bytes for clean downloading
                img_byte_arr = io.BytesIO()
                output_image.save(img_byte_arr, format='PNG')
                image_data = img_byte_arr.getvalue()
                
                # Clean Download Button
                st.download_button(
                    label="📥 Download HD Image",
                    data=image_data,
                    file_name="flux_output.png",
                    mime="image/png"
                )
                    
            except Exception as e:
                st.error(f"🚨 Connection Error: {e}")
                st.info("💡 If this persists, verify that your token in Streamlit Secrets has proper 'Read' permissions on Hugging Face.")
    elif generate_btn and not prompt:
        st.warning("⚠️ Please write a detailed prompt instruction first!")
        
