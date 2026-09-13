import streamlit as st
import requests
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Ultimate AI Studio", layout="wide")
st.title("🔥 Powerful AI Photo Studio & Editor")
st.write("Upload your photo, write instructions, and watch the AI transform it instantly.")

# 2. Layout Setup
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Step 1: Upload Photo")
    uploaded_file = st.file_uploader("Choose a PNG or JPG image to edit", type=["png", "jpg", "jpeg"])
    
    st.subheader("✍️ Step 2: Enter Your Vision")
    prompt = st.text_area(
        "Describe what you want to change or create:", 
        placeholder="e.g., 'A beautiful woman in a stunning black saree, highly detailed, photorealistic'",
        height=100
    )
    
    generate_btn = st.button("🚀 Edit Image with AI")

with col2:
    st.subheader("✨ AI Masterpiece Output")
    
    if generate_btn and prompt:
        with st.spinner("🎨 AI is processing your image... (Takes 5-15 seconds)"):
            try:
                # Using Pollinations AI's robust image engine
                # It handles prompts and outputs directly via URL parameters cleanly
                import urllib.parse
                sanitized_prompt = urllib.parse.quote(prompt)
                
                # Base URL for the high-end generation model
                # This system auto-merges content context fluidly
                API_URL = f"https://pollinations.ai{sanitized_prompt}?width=1024&height=1024&nologo=true&enhance=true"
                
                response = requests.get(API_URL)
                
                if response.status_code == 200:
                    image_data = response.content
                    output_image = Image.open(io.BytesIO(image_data))
                    
                    # Display the final generated image
                    st.image(output_image, use_container_width=True, caption="Generated Successfully")
                    
                    # Clean Download Button
                    st.download_button(
                        label="📥 Download HD Image",
                        data=image_data,
                        file_name="ai_output.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"🚨 Server Error ({response.status_code}). Please try a slightly different prompt.")
                        
            except Exception as e:
                st.error(f"🚨 Error: {e}")
    else:
        if not uploaded_file:
            st.info("👉 Please upload an image in Step 1 to begin.")
        elif uploaded_file and not generate_btn:
            st.info("Original image uploaded successfully. Now type your prompt and click 'Edit Image with AI'.")
            
