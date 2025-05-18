from .gemini_helper import GeminiHelper
import json
from PIL import Image
import io

async def estimate_nutrition(image_data):
    """
    Estimate nutrition information from a food image using Gemini Vision API.
    Returns a dictionary with estimated nutrition values and confidence score.
    """
    try:
        # Prepare the prompt for the vision model
        prompt = """
        Analyze this food image and provide nutritional information in the following JSON format:
        {
            "calories": number (estimated calories),
            "protein": number (grams of protein),
            "carbs": number (grams of carbohydrates),
            "fat": number (grams of fat),
            "confidence": number (between 0 and 1, indicating confidence in the estimation)
        }
        Be conservative in your estimates and provide realistic values based on typical serving sizes.
        Consider the portion size visible in the image.
        If multiple food items are present, provide combined nutritional values.
        """
        
        # Get response from Gemini Vision
        response = await GeminiHelper.analyze_image(image_data, prompt)
        
        # Parse the JSON response
        # Find the first occurrence of a JSON-like structure
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        json_str = response[start_idx:end_idx]
        
        # Parse the JSON data
        nutrition_data = json.loads(json_str)
        
        # Ensure all required fields are present with default values
        required_fields = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'confidence': 0.5
        }
        
        for field, default_value in required_fields.items():
            if field not in nutrition_data or not isinstance(nutrition_data[field], (int, float)):
                nutrition_data[field] = default_value
        
        return nutrition_data
        
    except Exception as e:
        raise Exception(f"Error estimating nutrition: {str(e)}")

def estimate_nutrition_sync(image_data):
    """
    Synchronous wrapper for estimate_nutrition function.
    Args:
        image_data: Either a PIL Image object or bytes of image data
    Returns:
        Dictionary containing nutrition information
    """
    import asyncio
    
    # If image_data is a PIL Image, convert it to bytes
    if isinstance(image_data, Image.Image):
        img_byte_arr = io.BytesIO()
        image_data.save(img_byte_arr, format='JPEG')
        image_data = img_byte_arr.getvalue()
    
    return asyncio.run(estimate_nutrition(image_data)) 