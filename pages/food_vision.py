# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error("Please set your GEMINI_API_KEY in the .env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def analyze_food_image(image):
    """Analyze food image using Gemini 1.5 Flash"""
    try:
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
        
        # Generate response
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def app():
    st.title("🍽️ Food Vision Analysis")
    st.write("Upload a food image or capture one using your camera to get detailed nutritional information.")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📤 Upload Image", "📸 Take Photo"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Analyze Uploaded Image"):
                with st.spinner("Analyzing image..."):
                    result = analyze_food_image(image)
                    st.markdown("### Analysis Results")
                    st.write(result)
    
    with tab2:
        camera_input = st.camera_input("Take a photo of your food")
        if camera_input is not None:
            image = Image.open(camera_input)
            st.image(image, caption="Captured Image", use_column_width=True)
            
            if st.button("Analyze Captured Image"):
                with st.spinner("Analyzing image..."):
                    result = analyze_food_image(image)
                    st.markdown("### Analysis Results")
                    st.write(result)

if __name__ == "__main__":
    app() 