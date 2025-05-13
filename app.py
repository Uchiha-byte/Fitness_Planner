import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from PIL import Image
import io
import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="ZFIT AI POWERED FITNESS TRACKER AND PLANNER",
    page_icon="💪",
    layout="wide"
)

# Load external CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS file
load_css('static/css/style.css')

# Initialize session state
if 'workout_plans' not in st.session_state:
    st.session_state.workout_plans = []
if 'nutrition_logs' not in st.session_state:
    st.session_state.nutrition_logs = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Exercise Library", "Nutrition Tracker", "Workout Planner", "AI Coach", "Food Vision"],
    icons=["house", "activity", "calculator", "calendar-check", "robot", "camera"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#1e2129"
        },
        "nav-link-selected": {"background-color": "#4c9aff"},
    }
)

# Home Page
if selected == "Home":
    # Hero Section
    st.markdown('<h1 class="title-text">Welcome to ZFIT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Your Personal AI Fitness Coach & Nutrition Guide</p>', unsafe_allow_html=True)

    # Quick Stats
    st.subheader("🌟 Platform Statistics")
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Exercises</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">100+</div>
            <div class="stat-label">AI Models</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">AI Support</div>
        </div>
        """, unsafe_allow_html=True)

    # Main Features
    st.subheader("💪 Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">🏋️‍♂️ Smart Exercise Library</h3>
            <p class="feature-text">
            Access a comprehensive database of exercises with detailed instructions and AI-powered recommendations.
            Features include:
            • HD video demonstrations
            • Real-time form correction
            • Difficulty progression tracking
            • Customized recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">🍎 Intelligent Nutrition Tracking</h3>
            <p class="feature-text">
            Track your meals and receive personalized dietary recommendations.
            Features include:
            • Food image recognition
            • Macro and micronutrient tracking
            • Meal planning assistance
            • Dietary restriction support
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">📊 Custom Workout Planning</h3>
            <p class="feature-text">
            Get AI-generated workout plans that adapt to your progress and goals.
            Features include:
            • Personalized workout schedules
            • Progress-based adjustments
            • Recovery monitoring
            • Goal tracking dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">🤖 AI Personal Coach</h3>
            <p class="feature-text">
            Receive real-time guidance and motivational support from our AI system.
            Features include:
            • 24/7 AI assistance
            • Personalized motivation
            • Form correction feedback
            • Progress insights
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Getting Started Section
    st.subheader("🚀 Getting Started")
    st.markdown("""
    <div class="feature-card">
    <ol>
        <li><strong>Explore Features:</strong> Navigate through our comprehensive features using the menu above</li>
        <li><strong>Set Your Goals:</strong> Define your fitness objectives and preferences</li>
        <li><strong>Start Your Journey:</strong> Begin with AI-recommended workouts and nutrition plans</li>
        <li><strong>Track Progress:</strong> Monitor your improvements and adjust your plans</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# Exercise Library
elif selected == "Exercise Library":
    st.header("Exercise Library")
    
    # Exercise categories
    exercise_category = st.selectbox(
        "Select Body Part",
        ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core", "Full Body"]
    )
    
    # Sample exercise data (in real app, this would come from a database)
    exercises = {
        "Chest": ["Bench Press", "Push-Ups", "Dumbbell Flyes", "Incline Press"],
        "Back": ["Pull-Ups", "Rows", "Lat Pulldowns", "Deadlifts"],
        "Legs": ["Squats", "Lunges", "Leg Press", "Calf Raises"],
        "Shoulders": ["Military Press", "Lateral Raises", "Front Raises"],
        "Arms": ["Bicep Curls", "Tricep Extensions", "Hammer Curls"],
        "Core": ["Planks", "Crunches", "Russian Twists", "Leg Raises"],
        "Full Body": ["Burpees", "Mountain Climbers", "Turkish Get-Ups"]
    }
    
    for exercise in exercises[exercise_category]:
        with st.expander(exercise):
            st.write(f"Description of {exercise} with proper form and technique.")
            st.write("Sets: 3-4")
            st.write("Reps: 8-12")
            st.write("Rest: 60-90 seconds")

# Placeholder for other sections
elif selected == "Nutrition Tracker":
    st.header("Nutrition Tracker")
    
    # Add new food entry
    with st.form("nutrition_entry"):
        st.subheader("Add Food Entry")
        col1, col2 = st.columns(2)
        with col1:
            food_name = st.text_input("Food Name")
            calories = st.number_input("Calories", min_value=0)
            protein = st.number_input("Protein (g)", min_value=0.0)
            fats = st.number_input("Fats (g)", min_value=0.0)
        with col2:
            carbs = st.number_input("Carbs (g)", min_value=0.0)
            sugar = st.number_input("Sugar (g)", min_value=0.0)
            serving_size = st.number_input("Serving Size (g)", min_value=0)
        
        submitted = st.form_submit_button("Add Entry")
        if submitted:
            new_entry = {
                "food_name": food_name,
                "calories": calories,
                "protein": protein,
                "fats": fats,
                "carbs": carbs,
                "sugar": sugar,
                "serving_size": serving_size,
                "date": pd.Timestamp.now().date()
            }
            st.session_state.nutrition_logs.append(new_entry)
            st.success("Food entry added successfully!")

    # Display nutrition summary
    if st.session_state.nutrition_logs:
        st.subheader("Today's Nutrition Summary")
        df = pd.DataFrame(st.session_state.nutrition_logs)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Calories", f"{df['calories'].sum():.0f}")
        with col2:
            st.metric("Total Protein", f"{df['protein'].sum():.1f}g")
        with col3:
            st.metric("Total Carbs", f"{df['carbs'].sum():.1f}g")
        with col4:
            st.metric("Total Fats", f"{df['fats'].sum():.1f}g")
        
        # Nutrition breakdown pie chart
        fig = px.pie(
            values=[df['protein'].sum(), df['carbs'].sum(), df['fats'].sum()],
            names=['Protein', 'Carbs', 'Fats'],
            title='Macronutrient Distribution'
        )
        st.plotly_chart(fig)

elif selected == "Workout Planner":
    st.header("Workout Planner")
    
    tab1, tab2 = st.tabs(["Create Plan", "My Plans"])
    
    with tab1:
        with st.form("workout_plan"):
            plan_name = st.text_input("Plan Name")
            duration = st.selectbox("Duration (weeks)", options=[1, 2, 4, 8, 12])
            frequency = st.selectbox("Workouts per week", options=[2, 3, 4, 5, 6])
            goal = st.selectbox("Goal", ["Strength", "Hypertrophy", "Weight Loss", "Endurance"])
            
            st.subheader("Workout Structure")
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            workout_days = {}
            
            for day in days:
                col1, col2 = st.columns(2)
                with col1:
                    workout_days[day] = st.checkbox(day)
                with col2:
                    if workout_days[day]:
                        st.selectbox(f"Focus for {day}", ["Rest", "Upper Body", "Lower Body", "Full Body", "Cardio"])
            
            submitted = st.form_submit_button("Create Plan")
            if submitted:
                new_plan = {
                    "name": plan_name,
                    "duration": duration,
                    "frequency": frequency,
                    "goal": goal,
                    "schedule": workout_days
                }
                st.session_state.workout_plans.append(new_plan)
                st.success("Workout plan created successfully!")
    
    with tab2:
        if st.session_state.workout_plans:
            for plan in st.session_state.workout_plans:
                with st.expander(plan["name"]):
                    st.write(f"Duration: {plan['duration']} weeks")
                    st.write(f"Frequency: {plan['frequency']} workouts/week")
                    st.write(f"Goal: {plan['goal']}")
                    st.write("Schedule:")
                    for day, selected in plan["schedule"].items():
                        if selected:
                            st.write(f"- {day}")
        else:
            st.info("No workout plans created yet. Create your first plan in the 'Create Plan' tab!")

elif selected == "AI Coach":
    st.header("AI Coach")
    
    # Initialize chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your fitness question..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response
        with st.chat_message("assistant"):
            response = "I'm your AI fitness coach! I can help you with workout plans, nutrition advice, and general fitness guidance. What would you like to know?"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

elif selected == "Food Vision":
    st.header("Food Vision - Nutrition Estimation")
    
    uploaded_file = st.file_uploader("Upload a picture of your food", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Food Image", use_column_width=True)
        
        # Placeholder for AI analysis
        st.info("Analyzing image...")
        
        # Placeholder results (in real app, this would use a trained model)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Estimated Nutrition Facts")
            st.write("Calories: ~300 kcal")
            st.write("Protein: 15g")
            st.write("Carbs: 40g")
            st.write("Fat: 10g")
        
        with col2:
            st.subheader("Identified Foods")
            st.write("• Main dish detected")
            st.write("• Side ingredients detected")
            st.write("Note: These are AI-generated estimates. Actual values may vary.") 