import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_VISION_MODEL

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class GeminiHelper:
    @staticmethod
    def get_text_model():
        """Get the text-only Gemini model."""
        return genai.GenerativeModel(GEMINI_MODEL)

    @staticmethod
    def get_vision_model():
        """Get the multimodal Gemini model for vision tasks."""
        return genai.GenerativeModel(GEMINI_VISION_MODEL)

    @staticmethod
    async def generate_response(prompt, temperature=0.7):
        """Generate a text response using Gemini."""
        model = GeminiHelper.get_text_model()
        response = await model.generate_content(prompt, temperature=temperature)
        return response.text

    @staticmethod
    async def analyze_image(image_data, prompt, temperature=0.7):
        """Analyze an image and generate a response using Gemini Vision."""
        model = GeminiHelper.get_vision_model()
        response = await model.generate_content([prompt, image_data], temperature=temperature)
        return response.text 