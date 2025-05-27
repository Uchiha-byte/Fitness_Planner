"""
Main application file
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime, timedelta

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="ZFIT AI POWERED FITNESS TRACKER AND PLANNER",
    page_icon="💪",
    layout="wide"
)

# Clear cache and session state for fresh reload
st.cache_data.clear()
if not st.session_state.get('app_init'):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.app_init = True

# Initialize session state for fitness goals if not exists
if 'fitness_goals' not in st.session_state:
    st.session_state.fitness_goals = {
        'weight': {'current': 80, 'target': 75, 'unit': 'kg'},
        'calories': {'daily': 2200, 'burned': 1800, 'unit': 'kcal'},
        'workouts': {'weekly_target': 4, 'completed': 3, 'unit': 'sessions'},
        'steps': {'daily_target': 10000, 'current': 8500, 'unit': 'steps'}
    }

# Initialize workout logs if not exists
if 'workout_logs' not in st.session_state:
    st.session_state.workout_logs = [
        {'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
         'type': ['Strength', 'Cardio', 'HIIT', 'Rest', 'Strength', 'Cardio', 'Rest'][i],
         'duration': [60, 45, 30, 0, 60, 45, 0][i],
         'calories': [400, 300, 250, 0, 400, 300, 0][i]}
        for i in range(7)
    ]

# Add URL parameter handling using the new st.query_params
if 'nav' in st.query_params:
    nav_value = st.query_params['nav']
    if nav_value in ["Exercise Library", "Workout Planner", "Nutrition Tracker", "AI Coach", "Food Vision"]:
        st.session_state.nav_selection = nav_value
        # Clear the URL parameter after handling
        st.query_params.clear()

try:
    # Import pages
    from pages.exercise_library import app as exercise_library_app
    from pages.workout_planner import app as workout_planner_app
    from pages.nutrition_tracker import app as nutrition_tracker_app
    from pages.ai_coach import app as ai_coach_app
    from pages.food_vision import app as food_vision_app
except ImportError as e:
    st.error(f"Error importing pages: {str(e)}")
    st.stop()

# Load external CSS
def load_css(css_file):
    try:
        with open(css_file, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Error loading CSS: {str(e)}")

# Load CSS file
load_css('static/css/style.css')

# Initialize session state for navigation
if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = 'Home'

# Navigation state management
def navigate_to(page_name):
    st.session_state.nav_selection = page_name
    # Update URL when navigation changes using the new st.query_params
    st.query_params['nav'] = page_name

# Sidebar with Logo
with st.sidebar:
    st.markdown("""
        <div class="zfit-logo">
            <h1 class="zfit-title">ZFIT</h1>
            <div class="zfit-divider"></div>
            <p class="zfit-slogan">Transform Your Life</p>
            <p class="zfit-subtitle">AI-Powered Fitness & Nutrition Coach</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button('🏠 Back to Home', use_container_width=True):
        navigate_to('Home')
        st.rerun()

    # Quick Access Menu
    st.markdown("""
        <div class="sidebar-menu">
            <div class="menu-item">
                <i>📊</i>
                <span class="menu-item-text">Dashboard Overview</span>
            </div>
            <div class="menu-item">
                <i>💪</i>
                <span class="menu-item-text">Workout Programs</span>
            </div>
            <div class="menu-item">
                <i>🥗</i>
                <span class="menu-item-text">Nutrition Plans</span>
            </div>
            <div class="menu-item">
                <i>📈</i>
                <span class="menu-item-text">Progress Tracking</span>
            </div>
            <div class="menu-item">
                <i>🤖</i>
                <span class="menu-item-text">AI Coach</span>
            </div>
        </div>

        <div class="sidebar-footer">
            <p>Version 2.0 | Powered by AI</p>
            <p>© 2025 ZFIT. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

# Get the current navigation index
current_index = ["Home", "Exercise Library", "Workout Planner", "Nutrition Tracker", "AI Coach", "Food Vision"].index(st.session_state.nav_selection)

# Top Navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Exercise Library", "Workout Planner", "Nutrition Tracker", "AI Coach", "Food Vision"],
    icons=["house", "activity", "calendar-check", "calculator", "robot", "camera"],
    menu_icon="cast",
    default_index=current_index,
    orientation="horizontal",
    key=f"nav_menu_{st.session_state.nav_selection}",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#ffffff", "font-size": "20px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "padding": "10px",
            "--hover-color": "transparent",
            "color": "#718096",
            "background-color": "transparent"
        },
        "nav-link-selected": {
            "background-color": "transparent",
            "color": "#4c9aff",
            "font-weight": "600",
            "border-bottom": "2px solid #4c9aff"
        },
    }
)

# Update navigation if changed through menu
if selected != st.session_state.nav_selection:
    navigate_to(selected)
    st.rerun()

# Main Content Area
if st.session_state.nav_selection == "Home":
    # Hero Section with Gradient Background
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">Welcome to ZFIT</h1>
            <p class="hero-subtitle">Your AI-Powered Fitness Journey Starts Here</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Single Horizontal Motivation Block
    st.markdown("""
    <div class="motivation-block">
        <div class="motivation-content">
            <div class="motivation-icon-group">
                <span class="motivation-emoji">💪</span>
                <span class="motivation-emoji">🎯</span>
                <span class="motivation-emoji">⭐</span>
            </div>
            <h2 class="motivation-heading">Today's Motivation</h2>
            <p class="motivation-quote">"The only bad workout is the one that didn't happen. Start today, and your future self will thank you. Remember: small progress is still progress!"</p>
            <div class="motivation-footer">
                <span class="motivation-author">ZFIT AI Coach</span>
                <span class="motivation-divider">•</span>
                <span class="motivation-date">Daily Inspiration</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Features Section
    st.markdown("<div class='features-section'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Exercise Library Card
        st.markdown("""
        <div class="feature-card workout">
            <div class="feature-content">
                <h3>🏋️‍♂️ Exercise Library</h3>
                <p>Access our comprehensive collection of exercises with AI-powered form guidance.</p>
                <ul class="feature-highlights">
                    <li>500+ Exercise Demonstrations</li>
                    <li>Real-time Form Analysis</li>
                    <li>Personalized Recommendations</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Exercises →", key="explore_exercises", use_container_width=True):
            navigate_to("Exercise Library")
            st.rerun()
        
        # Workout Planner Card
        st.markdown("""
        <div class="feature-card planner">
            <div class="feature-content">
                <h3>📊 Smart Workout Planner</h3>
                <p>Create custom workout plans tailored to your goals and preferences.</p>
                <ul class="feature-highlights">
                    <li>AI-Generated Programs</li>
                    <li>Progress Tracking</li>
                    <li>Adaptive Difficulty</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Plan Workout →", key="plan_workout", use_container_width=True):
            navigate_to("Workout Planner")
            st.rerun()

    with col2:
        # Nutrition Tracker Card
        st.markdown("""
        <div class="feature-card nutrition">
            <div class="feature-content">
                <h3>🍎 Nutrition Tracker</h3>
                <p>Track your meals and get personalized nutrition advice.</p>
                <ul class="feature-highlights">
                    <li>Smart Meal Recognition</li>
                    <li>Macro Tracking</li>
                    <li>Personalized Diet Plans</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Track Nutrition →", key="track_nutrition", use_container_width=True):
            navigate_to("Nutrition Tracker")
            st.rerun()
        
        # AI Coach Card
        st.markdown("""
        <div class="feature-card ai-coach">
            <div class="feature-content">
                <h3>🤖 AI Coach</h3>
                <p>Get real-time guidance and motivation from your personal AI coach.</p>
                <ul class="feature-highlights">
                    <li>24/7 Availability</li>
                    <li>Personalized Advice</li>
                    <li>Goal Setting & Tracking</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Talk to Coach →", key="talk_to_coach", use_container_width=True):
            navigate_to("AI Coach")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.nav_selection == "Exercise Library":
    exercise_library_app()
elif st.session_state.nav_selection == "Workout Planner":
    workout_planner_app()
elif st.session_state.nav_selection == "Nutrition Tracker":
    nutrition_tracker_app()
elif st.session_state.nav_selection == "AI Coach":
    ai_coach_app()
elif st.session_state.nav_selection == "Food Vision":
    food_vision_app() 



