# -*- coding: utf-8 -*-
import streamlit as st
from PIL import Image
import io
from utils import estimate_nutrition
from config import GEMINI_API_KEY

def app():
    st.title("Food Vision")
    
    st.info("""
    🚧 This feature is currently under maintenance.
    
    The Food Vision feature requires TensorFlow, which is not yet compatible with Python 3.13.2.
    We're working on making this feature available in a future update.
    
    In the meantime, you can still use all other features of the application!
    """)
    
    st.markdown("""
    ### Coming Soon:
    - Food recognition from images
    - Automatic nutrition facts calculation
    - Quick and easy meal logging
    - Integration with nutrition tracker
    """)
    
    # Check if Gemini API key is configured
    if GEMINI_API_KEY == "your-gemini-api-key-here":
        st.error("Please configure your Gemini API key in config.py")
        return
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a picture of your food", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Food Image", use_column_width=True)
            
            # Add a button to trigger analysis
            if st.button("Analyze Image"):
                with st.spinner("Analyzing your food using Gemini Vision AI..."):
                    try:
                        # Get nutrition estimation
                        nutrition_info = estimate_nutrition(image)
                        
                        # Display results in a nice format
                        st.success("Analysis complete!")
                        
                        # Display confidence score
                        confidence = min(max(nutrition_info['confidence'], 0), 1)  # Ensure between 0 and 1
                        st.progress(confidence)
                        st.caption(f"Confidence Score: {confidence*100:.1f}%")
                        
                        # Display nutrition information
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Estimated Nutrition Facts")
                            st.write(f"**Calories:** {nutrition_info['calories']:.0f} kcal")
                            st.write(f"**Protein:** {nutrition_info['protein']:.1f}g")
                            st.write(f"**Carbs:** {nutrition_info['carbs']:.1f}g")
                            st.write(f"**Fat:** {nutrition_info['fat']:.1f}g")
                        
                        with col2:
                            # Add a pie chart for macronutrient distribution
                            import plotly.express as px
                            
                            # Calculate total macros
                            total_macros = (nutrition_info['protein'] * 4 + 
                                          nutrition_info['carbs'] * 4 + 
                                          nutrition_info['fat'] * 9)
                            
                            if total_macros > 0:
                                # Calculate percentages
                                protein_pct = (nutrition_info['protein'] * 4 / total_macros) * 100
                                carbs_pct = (nutrition_info['carbs'] * 4 / total_macros) * 100
                                fat_pct = (nutrition_info['fat'] * 9 / total_macros) * 100
                                
                                fig = px.pie(
                                    values=[protein_pct, carbs_pct, fat_pct],
                                    names=['Protein', 'Carbs', 'Fat'],
                                    title='Macronutrient Distribution (%)'
                                )
                                st.plotly_chart(fig)
                        
                        # Add button to log this food
                        if st.button("Add to Nutrition Log"):
                            if "nutrition_logs" not in st.session_state:
                                st.session_state.nutrition_logs = []
                            
                            # Add to nutrition log
                            from datetime import datetime
                            new_entry = {
                                "food_name": "Food from image",
                                "calories": nutrition_info['calories'],
                                "protein": nutrition_info['protein'],
                                "carbs": nutrition_info['carbs'],
                                "fat": nutrition_info['fat'],
                                "date": datetime.now().date(),
                                "meal_type": "Other",
                                "source": "Food Vision"
                            }
                            st.session_state.nutrition_logs.append(new_entry)
                            st.success("Added to your nutrition log!")
                    
                    except Exception as e:
                        st.error(f"Error analyzing image: {str(e)}")
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    else:
        # Display instructions and tips
        st.info("""
        ### Tips for best results:
        - Take photos in good lighting
        - Center the food in the image
        - Try to include all items in a single shot
        - Avoid blurry images
        - Include common objects for size reference
        """)
        
        # Display sample images
        st.subheader("Example Images")
        st.write("Take clear, well-lit photos of your food for the most accurate nutrition estimates.")

if __name__ == "__main__":
    app() 