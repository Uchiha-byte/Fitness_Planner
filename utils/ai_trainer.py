import google.generativeai as genai
import os
import json
import requests
from typing import Dict, List, Any

class AITrainer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def _make_api_request(self, prompt: str) -> Dict:
        """Make API request to Gemini."""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def _parse_json_response(self, response_text: str) -> Dict:
        """Helper method to parse JSON from response text."""
        try:
            # Clean the response text
            clean_text = response_text.strip()
            if "```json" in clean_text:
                clean_text = clean_text.split("```json")[1].split("```")[0]
            elif "```" in clean_text:
                clean_text = clean_text.split("```")[1].split("```")[0]
            return json.loads(clean_text)
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return None

    def generate_workout_program(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete workout program based on user preferences."""
        prompt = f"""
        As an expert fitness trainer, create a detailed {user_input.get('duration_weeks', 4)}-week workout program following these specifications:

        USER PROFILE:
        • Goal: {user_input.get('goal', 'General Fitness')}
        • Experience Level: {user_input.get('fitness_level', 'Beginner')}
        • Available Equipment: {', '.join(user_input.get('equipment', ['Bodyweight']))}
        • Training Frequency: {user_input.get('days_per_week', 3)} days per week
        • Session Duration: {user_input.get('time_per_session', 45)} minutes

        REQUIREMENTS:
        1. Focus on proper exercise progression
        2. Include compound movements as primary exercises
        3. Balance workout intensity and recovery
        4. Provide clear exercise order and rest periods
        5. Include form cues and safety notes
        6. Ensure exercises match available equipment
        7. Structure workouts to fit within time limit
        8. Include warm-up and cool-down recommendations

        Please generate a structured workout program in the following JSON format:
        {{
            "name": "Program name reflecting the goal",
            "description": "Detailed program overview including key features and expected outcomes",
            "frequency": "X days/week",
            "duration_weeks": number,
            "difficulty": "Beginner/Intermediate/Advanced",
            "tags": ["relevant", "program", "tags"],
            "workout_days": [
                {{
                    "day_number": 1,
                    "name": "Focus of the day (e.g., Push, Pull, etc.)",
                    "exercises": [
                        {{
                            "name": "Exercise name",
                            "sets": number,
                            "reps": "number or range (e.g., '8-12')",
                            "rest_seconds": number,
                            "notes": "Form cues, breathing pattern, and safety tips",
                            "order": number
                        }}
                    ]
                }}
            ]
        }}

        IMPORTANT GUIDELINES:
        • Start with easier exercises and progress in complexity
        • Include proper warm-up exercises for each session
        • Provide specific rest periods between sets and exercises
        • Add detailed form cues for each exercise
        • Consider user's experience level when selecting exercises
        • Ensure exercises flow logically within each session
        • Include progressive overload recommendations
        • Add alternative exercises for equipment flexibility
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error generating workout program: {e}")
            return None

    def suggest_workout_modifications(self, workout_data: Dict[str, Any], user_feedback: str) -> Dict[str, Any]:
        """Suggest modifications to a workout based on user feedback."""
        prompt = f"""
        As an expert fitness trainer, analyze this workout data and user feedback to suggest modifications:
        
        Current Workout:
        {json.dumps(workout_data, indent=2)}
        
        User Feedback:
        {user_feedback}
        
        Provide modifications in JSON format:
        {{
            "modifications": [
                {{
                    "exercise": "Original exercise name",
                    "change": "What to change",
                    "reason": "Why make this change",
                    "alternative": "Alternative exercise or modification"
                }}
            ],
            "general_advice": "Overall advice for improvement"
        }}
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error suggesting modifications: {e}")
            return None

    def generate_form_tips(self, exercise_name: str) -> Dict[str, Any]:
        """Generate detailed form tips and common mistakes for an exercise."""
        prompt = f"""
        As an expert fitness trainer, provide detailed form instructions and tips for the {exercise_name} exercise.
        Include setup, execution, common mistakes, and safety considerations.
        
        Provide the information in JSON format:
        {{
            "exercise": "{exercise_name}",
            "setup": ["Step-by-step setup instructions"],
            "execution": ["Step-by-step execution points"],
            "common_mistakes": ["List of common mistakes"],
            "safety_tips": ["Important safety considerations"],
            "breathing": "Breathing pattern instructions",
            "variations": ["Possible variations or progressions"]
        }}
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error generating form tips: {e}")
            return None

    def analyze_workout_performance(self, workout_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workout performance and provide insights."""
        prompt = f"""
        As an expert fitness trainer, analyze this workout performance data and provide insights:
        
        Workout Data:
        {json.dumps(workout_data, indent=2)}
        
        Provide analysis in JSON format:
        {{
            "overall_performance": "General performance assessment",
            "achievements": ["List of notable achievements"],
            "areas_for_improvement": ["Areas that need work"],
            "recommendations": ["Specific recommendations"],
            "next_session_tips": ["Tips for the next workout"]
        }}
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error analyzing performance: {e}")
            return None 