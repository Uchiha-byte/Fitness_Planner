import openai
from config import OPENAI_API_KEY

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

def generate_ai_response(prompt, context="", model="gpt-3.5-turbo"):
    """Generate an AI response using OpenAI's API."""
    try:
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating AI response: {str(e)}") 