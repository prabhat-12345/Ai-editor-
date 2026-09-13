import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Ultimate AI Studio", layout="wide")
st.title("🔥 FLUX AI Photo Studio & Editor")
st.write("Upload your photo, write instructions, and let the AI edit it perfectly.")

# 2. Loading Secret API Key Safely from Streamlit Cloud Secrets
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except Exception:
    st.error("🚨 Configuration Missing: Please add 'HF_API_KEY' in your Streamlit Cloud Settings -> Secrets!")
    st.stop()

# Using Official Hugging Face Client for reliable img2img connections
@st.cache_resource
def get_ai_client(api_key):
    return InferenceClient(token=api_key)

client = get_ai_client(HF_API_KEY)

# 3. Layout Setup
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Step 1: Upload Photo")
    # यहाँ आ गया असली फोटो अपलोड का बटन
    uploaded_file = st.file_uploader("Choose a PNG or JPG image to edit", type=["png", "jpg", "jpeg"])
    
    st.subheader("✍️ Step 2: Enter Your Vision")
    prompt = st.text_area(
        "Describe what you want to change or add to this photo:", 
        placeholder="e.g., 'Change the background to a rainy street' or 'Add sunglasses to the person'",
        height=100
    )
    
    generate_btn = st.button("🚀 Edit Image with AI")

with col2:
    st.subheader("✨ AI Masterpiece Output")
    
    if uploaded_file is not None:
        # Display the uploaded original image first
        st.info("Original image uploaded successfully.")
        
        if generate_btn and prompt:
            with st.spinner("🎨 FLUX AI is editing your photo... (Takes 10-25 seconds)"):
                try:
                    # Convert the uploaded file into raw bytes for the AI model
                    image_bytes = uploaded_file.getvalue()
                    
                    # Using the official image_to_image method (Bypasses errors and respects original image structure)
                    output_image = client.image_to_image(
                        image=image_bytes,
                        prompt=prompt,
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    
                    # Display the final generated image
                    st.image(output_image, use_container_width=True, caption="Successfully Edited via FLUX")
                    
                    # Convert image back to bytes for clean downloading
                    img_byte_arr = io.BytesIO()
                    output_image.save(img_byte_arr, format='PNG')
                    download_data = img_byte_arr.getvalue()
                    
                    # Clean Download Button
                    st.download_button(
                        label="📥 Download HD Image",
                        data=download_data,
                        file_name="flux_edited_output.png",
                        mime="image/png"
                    )
                        
                except Exception as e:
                    st.error(f"🚨 Connection Error: {e}")
                    st.info("💡 Ensure your Hugging Face fine-grained token has all proper permissions.")
        elif generate_btn and not prompt:
            st.warning("⚠️ Please write an editing instruction prompt first!")
    else:
        st.info("👉 Please upload an image in Step 1 to begin editing.")
        
