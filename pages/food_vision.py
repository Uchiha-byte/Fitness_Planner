# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error("Please set your GEMINI_API_KEY in the .env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def process_image(image_data):
    """Process image data from either file upload or camera input"""
    try:
        if isinstance(image_data, bytes):
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, Image.Image):
            # Already a PIL Image
            image = image_data
        else:
            raise ValueError("Unsupported image data type")
        
        # Convert to RGB if necessary (some images might be in RGBA or other modes)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        max_size = (800, 800)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return image
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def analyze_food_image(image):
    """Analyze food image using Gemini 1.5 Flash"""
    try:
        # Process the image first
        processed_image = process_image(image)
        if processed_image is None:
            return None
        
        # Initialize Gemini 1.5 Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare the prompt
        prompt = """Analyze this food image and provide the following information in a structured format:
        1. Name of the food
        2. Estimated calories per serving
        3. Macronutrients (in grams):
           - Carbohydrates
           - Proteins
           - Fats
        4. Key micronutrients
        5. Health benefits
        Please be as accurate as possible with the nutritional information."""
        
        # Set up generation config with supported parameters
        generation_config = {
            "temperature": 0.4,  # Lower temperature for more focused responses
            "top_p": 0.8,       # Nucleus sampling parameter
            "top_k": 40,        # Top-k sampling parameter
            "max_output_tokens": 1024,  # Maximum length of the response
        }
        
        # Generate response with retry logic
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    [prompt, processed_image],
                    generation_config=generation_config
                )
                
                if response and response.text:
                    return response.text
                else:
                    raise ValueError("Empty response from model")
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise e
                
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg:
            st.error("Invalid or missing API key. Please check your GEMINI_API_KEY in the .env file.")
        elif "quota" in error_msg.lower():
            st.error("API quota exceeded. Please try again later.")
        elif "timeout" in error_msg.lower():
            st.error("Request timed out. Please try again.")
        else:
            st.error(f"Error analyzing image: {error_msg}")
        return None

def app():
    st.title("🍽️ Food Vision Analysis")
    st.write("Upload a food image or capture one using your camera to get detailed nutritional information.")
    
    # Add a note about image requirements
    st.info("""
    💡 Tips for best results:
    - Use clear, well-lit images
    - Ensure the food is clearly visible
    - Avoid blurry or dark photos
    - Single food items work best
    """)
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📤 Upload Image", "📸 Take Photo"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                # Read image data
                image_data = uploaded_file.getvalue()
                # Process and display image
                image = process_image(image_data)
                if image:
                    st.image(image, caption="Uploaded Image", use_container_width=True)
                    
                    if st.button("Analyze Uploaded Image"):
                        with st.spinner("Analyzing image... This may take a few seconds."):
                            result = analyze_food_image(image_data)
                            if result:
                                st.markdown("### Analysis Results")
                                st.write(result)
                            else:
                                st.error("Failed to analyze the image. Please try again with a different image.")
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Please try uploading a different image.")
    
    with tab2:
        camera_input = st.camera_input("Take a photo of your food")
        if camera_input is not None:
            try:
                # Read image data
                image_data = camera_input.getvalue()
                # Process and display image
                image = process_image(image_data)
                if image:
                    st.image(image, caption="Captured Image", use_container_width=True)
                    
                    if st.button("Analyze Captured Image"):
                        with st.spinner("Analyzing image... This may take a few seconds."):
                            result = analyze_food_image(image_data)
                            if result:
                                st.markdown("### Analysis Results")
                                st.write(result)
                            else:
                                st.error("Failed to analyze the image. Please try again with a different image.")
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Please try taking a different photo.")

if __name__ == "__main__":
    app() 