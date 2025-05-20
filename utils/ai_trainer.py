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

    def _make_api_request(self, prompt: str, context: str = "") -> Dict:
        """Make API request to Gemini."""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def _parse_json_response(self, response_text: str) -> Dict:
        """Helper method to parse JSON from response text."""
        try:
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
        Create a strict, no-nonsense {user_input.get('duration_weeks', 4)}-week workout program:

        USER PROFILE:
        • Goal: {user_input.get('goal', 'General Fitness')}
        • Level: {user_input.get('fitness_level', 'Beginner')}
        • Equipment: {', '.join(user_input.get('equipment', ['Bodyweight']))}
        • Frequency: {user_input.get('days_per_week', 3)} days/week
        • Duration: {user_input.get('time_per_session', 45)} minutes

        REQUIREMENTS:
        1. Focus on compound movements
        2. Minimal rest between sets
        3. Progressive overload
        4. No fluff exercises
        5. Maximum efficiency
        6. Safety first
        7. Include specific form cues
        8. Add intensity techniques
        9. Include progress tracking metrics

        Generate in JSON format:
        {{
            "name": "Program name",
            "description": "Brief, direct program overview with key benefits and challenges",
            "frequency": "X days/week",
            "duration_weeks": number,
            "difficulty": "Beginner/Intermediate/Advanced",
            "tags": ["relevant", "tags"],
            "workout_days": [
                {{
                    "day_number": 1,
                    "name": "Focus (e.g., Push, Pull)",
                    "exercises": [
                        {{
                            "name": "Exercise name",
                            "sets": number,
                            "reps": "number or range",
                            "rest_seconds": number,
                            "notes": "Key form points, breathing pattern, and intensity technique",
                            "order": number,
                            "progression": "How to progress this exercise",
                            "target_muscles": ["Primary", "Secondary"],
                            "intensity_technique": "Optional technique to increase difficulty"
                        }}
                    ]
                }}
            ],
            "weekly_challenges": [
                {{
                    "week": number,
                    "challenge": "Specific challenge for the week",
                    "target": "Measurable goal"
                }}
            ],
            "progress_metrics": [
                "List of metrics to track progress"
            ]
        }}

        Keep it simple but include all necessary details for success.
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error generating workout program: {e}")
            return None

    def generate_nutrition_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a personalized nutrition plan."""
        prompt = f"""
        As an expert nutritionist, create a detailed nutrition plan following these specifications:

        USER PROFILE:
        • Goal: {user_profile.get('goal', 'General Health')}
        • Activity Level: {user_profile.get('activity_level', 'Moderate')}
        • Dietary Preferences: {user_profile.get('dietary_preferences', 'No restrictions')}
        • Allergies/Restrictions: {user_profile.get('restrictions', 'None')}
        • Daily Calorie Target: {user_profile.get('calories', 2000)} kcal

        REQUIREMENTS:
        1. Focus on whole, nutrient-dense foods
        2. Balance macronutrients appropriately
        3. Include meal timing recommendations
        4. Provide portion size guidance
        5. Include hydration recommendations
        6. Consider dietary preferences and restrictions
        7. Include supplement recommendations if needed
        8. Provide meal prep tips

        Please generate a structured nutrition plan in the following JSON format:
        {{
            "name": "Plan name reflecting the goal",
            "description": "Detailed plan overview",
            "daily_calories": number,
            "macronutrient_split": {{
                "protein": number,
                "carbs": number,
                "fat": number
            }},
            "meal_timing": [
                {{
                    "meal": "Meal name",
                    "timing": "When to eat",
                    "calories": number,
                    "macros": {{
                        "protein": number,
                        "carbs": number,
                        "fat": number
                    }},
                    "food_suggestions": ["List of recommended foods"],
                    "portion_guidelines": "Portion size recommendations"
                }}
            ],
            "hydration": {{
                "daily_water": "Amount in ml",
                "timing": ["When to drink"],
                "additional_fluids": ["Other recommended fluids"]
            }},
            "supplements": [
                {{
                    "name": "Supplement name",
                    "dosage": "Recommended dosage",
                    "timing": "When to take",
                    "purpose": "Why take this"
                }}
            ],
            "meal_prep_tips": ["List of meal prep recommendations"]
        }}
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error generating nutrition plan: {e}")
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

    def analyze_nutrition_log(self, nutrition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze nutrition log and provide insights."""
        prompt = f"""
        As an expert nutritionist, analyze this nutrition log data and provide insights:
        
        Nutrition Data:
        {json.dumps(nutrition_data, indent=2)}
        
        Provide analysis in JSON format:
        {{
            "overall_assessment": "General nutrition assessment",
            "strengths": ["Positive aspects of the diet"],
            "areas_for_improvement": ["Areas that need work"],
            "recommendations": ["Specific dietary recommendations"],
            "meal_timing_suggestions": ["Suggestions for meal timing"],
            "hydration_analysis": "Analysis of hydration habits"
        }}
        """

        try:
            response = self._make_api_request(prompt)
            if response and 'candidates' in response:
                return self._parse_json_response(response['candidates'][0]['content']['parts'][0]['text'])
            return None
        except Exception as e:
            print(f"Error analyzing nutrition log: {e}")
            return None 