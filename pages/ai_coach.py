# -*- coding: utf-8 -*-
"""
AI Coach Module
Provides AI-powered fitness coaching and guidance
"""

import streamlit as st
from utils.ai_trainer import AITrainer
from utils.workout_db import WorkoutDatabase
import json
import os
from datetime import datetime

def format_workout_data(workout_data):
    """Format workout data for AI context"""
    return f"""
    Workout History:
    - Total Workouts: {workout_data.get('total_workouts', 0)}
    - This Month: {workout_data.get('workouts_this_month', 0)}
    - Average Duration: {workout_data.get('avg_duration', 0)} minutes
    - Consistency: {workout_data.get('consistency', 0)}%
    """

def format_workout_plan(program):
    """Format workout plan into bold bullet points"""
    output = f"""
**{program['name']}**
**{program['description']}**

**Schedule:** {program['frequency']} for {program['duration_weeks']} weeks
**Difficulty:** {program['difficulty']}

"""
    for day in program['workout_days']:
        output += f"\n**Day {day['day_number']}: {day['name']}**\n"
        for ex in day['exercises']:
            if "warm-up" not in ex["name"].lower() and "cool-down" not in ex["name"].lower():
                output += f"• **{ex['name']}** - {ex['sets']} sets × {ex['reps']} reps (Rest: {ex['rest_seconds']}s)\n"
                if ex['notes']:
                    output += f"  *{ex['notes']}*\n"
    return output

def get_quick_assist_response(topic):
    """Get predefined responses for quick assist topics"""
    responses = {
        "form_check": """
**FORM CHECK GUIDELINES**

• **Record your form** from front, side, and 45° angles for comprehensive analysis

• **Focus on key points:**
  - Neutral spine alignment (no rounding, maintain natural curve)
  - Joint positioning (knees track toes, no inward collapse)
  - Full range of motion (complete movement, no partial reps)
  - Controlled breathing (exhale on exertion, maintain rhythm)

• **Submit video for review** with exercise name, weight used, and any specific concerns

• **Common mistakes to avoid:**
  - Rushing through movements
  - Using momentum instead of muscle control
  - Improper breathing patterns
  - Incomplete range of motion
""",
        "nutrition_tips": """
**NUTRITION BASICS**

• **Protein:** 1.6-2.2g per kg bodyweight
  - Sources: chicken, fish, eggs, Greek yogurt
  - Timing: 30g within 30 minutes post-workout
  - Distribution: 20-30g per meal

• **Carbs:** 3-5g per kg bodyweight
  - Sources: rice, oats, sweet potatoes, fruits
  - Timing: Higher around workouts
  - Focus: Complex carbs for sustained energy

• **Fats:** 0.5-1g per kg bodyweight
  - Sources: avocado, nuts, olive oil, fatty fish
  - Timing: Spread throughout day
  - Types: Focus on healthy unsaturated fats

• **Hydration:** 3-4L water daily
  - Add 500ml during workouts
  - Monitor urine color (light yellow)
  - Include electrolytes during intense sessions
""",
        "recovery": """
**RECOVERY PROTOCOL**

• **Sleep:** 7-9 hours minimum
  - Maintain consistent schedule
  - Dark, cool room (18-20°C)
  - No screens 1 hour before bed
  - Consider sleep tracking

• **Stretching:** 10-15 minutes daily
  - Focus on tight muscle groups
  - Hold stretches 30-60 seconds
  - Include dynamic and static stretches
  - Target major movement patterns

• **Foam rolling:** 2-3 minutes per muscle group
  - Perform 3x weekly
  - Focus on trigger points
  - Move slowly and deliberately
  - Breathe through discomfort

• **Active recovery:** 20-30 minutes light cardio
  - Walking, cycling, swimming
  - Keep heart rate below 120
  - Focus on movement quality
  - Include mobility work
""",
        "motivation": """
**STAY MOTIVATED**

• **Set specific goals** with clear metrics
  - Weekly and monthly targets
  - Progress photos every 2 weeks
  - Strength and endurance benchmarks
  - Body measurements tracking

• **Track progress** systematically
  - Daily workout log
  - Nutrition tracking
  - Sleep and recovery metrics
  - Energy levels and mood

• **Find a workout partner**
  - Share goals and progress
  - Schedule regular sessions
  - Create friendly competition
  - Hold each other accountable

• **Reward system**
  - Milestone celebrations
  - New workout gear
  - Recovery treatments
  - Progress photo comparisons
""",
        "injury_prevention": """
**INJURY PREVENTION**

• **Warm up properly**
  - 5-10 minutes dynamic stretching
  - Light cardio to raise body temperature
  - Movement-specific preparation
  - Gradual intensity increase

• **Progress gradually**
  - Increase weight by 5% weekly max
  - Add volume before intensity
  - Monitor form at all times
  - Listen to body signals

• **Maintain proper form**
  - Record and review technique
  - Focus on mind-muscle connection
  - Use mirrors or video feedback
  - Get regular form checks

• **Recovery management**
  - Rest if pain exceeds 3/10
  - Ice/heat as needed
  - Regular mobility work
  - Adequate sleep and nutrition
""",
        "plateau_break": """
**BREAK THROUGH PLATEAUS**

• **Increase intensity systematically**
  - Add 5-10% weight or reps
  - Reduce rest periods gradually
  - Increase training frequency
  - Add advanced techniques

• **Change exercise variables**
  - Rotate exercise order
  - Start with weak points
  - Add new variations
  - Modify grip/stance

• **Implement advanced techniques**
  - Supersets and giant sets
  - Drop sets and rest-pause
  - Eccentric focus
  - Time under tension

• **Optimize recovery**
  - Increase protein intake
  - Improve sleep quality
  - Add active recovery
  - Consider deload week
"""
    }
    return responses.get(topic, "Topic not found.")

def app():
    st.title("AI Fitness Coach")
    
    # Initialize database and AI trainer
    if 'workout_db' not in st.session_state:
        st.session_state.workout_db = WorkoutDatabase()
    
    if 'ai_trainer' not in st.session_state:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("Please set the GEMINI_API_KEY environment variable to use AI features.")
            return
        st.session_state.ai_trainer = AITrainer(api_key)
    
    # Initialize chat history in session state if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Get user's workout data for context
    workout_stats = st.session_state.workout_db.get_workout_statistics()
    workout_context = format_workout_data(workout_stats) if workout_stats else ""
    
    # Quick Assist Section with better organization
    st.subheader("Quick Assist")
    
    # Create two rows of buttons
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    # First row of buttons
    with row1_col1:
        if st.button("Form Check Guide", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("form_check")
            })
            st.rerun()
    
    with row1_col2:
        if st.button("Nutrition Tips", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("nutrition_tips")
            })
            st.rerun()
    
    with row1_col3:
        if st.button("Recovery Protocol", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("recovery")
            })
            st.rerun()
    
    # Second row of buttons
    with row2_col1:
        if st.button("Stay Motivated", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("motivation")
            })
            st.rerun()
    
    with row2_col2:
        if st.button("Injury Prevention", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("injury_prevention")
            })
            st.rerun()
    
    with row2_col3:
        if st.button("Break Plateaus", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": get_quick_assist_response("plateau_break")
            })
            st.rerun()
    
    # Add some spacing
    st.markdown("---")
    
    # Chat interface
    st.subheader("Chat with your AI Fitness Coach")
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your fitness question..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # Prepare context for the AI
            context = f"""
            You are a strict, no-nonsense fitness coach. Your responses should be:
            - Direct and to the point
            - Focused on actionable advice
            - Challenging but realistic
            - Evidence-based
            - No sugar-coating
            
            Current User Context:
            {workout_context}
            
            Response Guidelines:
            1. Keep responses between 80-120 words
            2. Format each point on a new line
            3. Use strong, commanding language
            4. No small talk or unnecessary explanations
            5. Prioritize form and safety
            6. Format responses in bold bullet points
            7. Include specific numbers and metrics
            8. Add motivational challenges
            9. Each point should be on its own line
            10. Use clear, concise language
            
            Example Format:
            **TITLE**
            
            • **Point 1** - Specific detail with additional information
            
            • **Point 2** - Specific detail with additional information
            
            • **Point 3** - Specific detail with additional information
            
            • **Point 4** - Specific detail with additional information
            """
            
            # Generate AI response
            response = st.session_state.ai_trainer._make_api_request(prompt, context)
            if response and 'candidates' in response:
                ai_response = response['candidates'][0]['content']['parts'][0]['text']
            else:
                ai_response = "Error generating response. Try again."
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
            # Display AI response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Quick action buttons
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Workout Plan"):
            with st.spinner("Creating your workout plan..."):
                user_input = {
                    'goal': 'General Fitness',
                    'fitness_level': 'Beginner',
                    'days_per_week': 3,
                    'time_per_session': 45,
                    'duration_weeks': 4,
                    'equipment': ['Bodyweight', 'Dumbbells']
                }
                program = st.session_state.ai_trainer.generate_workout_program(user_input)
                if program:
                    formatted_plan = format_workout_plan(program)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": formatted_plan
                    })
                    st.rerun()
    
    with col2:
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    app() 