import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_ai_response(prompt, context="", model="gemini-pro"):
    """Generate an AI response using Gemini API."""
    try:
        # Initialize the model
        model = genai.GenerativeModel(model)
        
        # Combine context and prompt
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"Error generating AI response: {str(e)}") 