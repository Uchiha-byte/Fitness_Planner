import numpy as np
from PIL import Image
import io
import tensorflow as tf
import openai
from datetime import datetime, timedelta
import pandas as pd

def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using the Mifflin-St Jeor Equation"""
    if gender.lower() == 'male':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }
    return bmr * activity_multipliers[activity_level.lower()]

def calculate_macros(calories, goal):
    """Calculate macronutrient distribution based on goal"""
    from config import NUTRITION_GOALS
    
    goal_data = NUTRITION_GOALS[goal]
    
    protein_cals = calories * goal_data['protein_ratio']
    carb_cals = calories * goal_data['carb_ratio']
    fat_cals = calories * goal_data['fat_ratio']
    
    return {
        'protein': round(protein_cals / 4),  # 4 calories per gram of protein
        'carbs': round(carb_cals / 4),      # 4 calories per gram of carbs
        'fats': round(fat_cals / 9)         # 9 calories per gram of fat
    }

def format_workout_plan(plan_data):
    """Format workout plan data for display"""
    formatted_plan = []
    for day, exercises in plan_data.items():
        if exercises:  # if there are exercises planned for this day
            formatted_plan.append(f"**{day}**")
            for exercise in exercises:
                formatted_plan.append(f"- {exercise['name']}: {exercise['sets']} sets x {exercise['reps']} reps")
            formatted_plan.append("")  # empty line for spacing
    return "\n".join(formatted_plan)

def get_progress_metrics(nutrition_logs):
    """Calculate progress metrics from nutrition logs"""
    df = pd.DataFrame(nutrition_logs)
    if df.empty:
        return None
    
    # Calculate daily averages
    daily_averages = df.groupby('date').agg({
        'calories': 'sum',
        'protein': 'sum',
        'carbs': 'sum',
        'fats': 'sum'
    }).mean()
    
    # Calculate compliance percentage
    total_days = (df['date'].max() - df['date'].min()).days + 1
    logged_days = df['date'].nunique()
    compliance = (logged_days / total_days) * 100 if total_days > 0 else 0
    
    return {
        'daily_averages': daily_averages.to_dict(),
        'compliance': round(compliance, 1)
    }

def generate_ai_response(prompt, context=None):
    """Generate AI response using OpenAI API"""
    try:
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm having trouble generating a response right now. Error: {str(e)}"

def preprocess_food_image(image):
    """Preprocess food image for model prediction"""
    # Resize image to expected dimensions
    target_size = (224, 224)
    image = image.resize(target_size)
    
    # Convert to array and preprocess
    img_array = np.array(image)
    img_array = img_array / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    return img_array

def estimate_nutrition(predictions, confidence_threshold=0.5):
    """Estimate nutrition facts based on model predictions"""
    # This is a placeholder function that would normally use a real model
    # and database of nutritional information
    sample_nutrition = {
        'calories': 300,
        'protein': 15,
        'carbs': 40,
        'fat': 10,
        'confidence': 0.85
    }
    return sample_nutrition 