"""
Main application file
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime, timedelta
from utils.db_manager import get_user_by_id, update_user_profile

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

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user' not in st.session_state:
    st.session_state.user = None

# Initialize session state for fitness goals based on user data if authenticated
if st.session_state.authenticated and st.session_state.user:
    user = st.session_state.user
    if 'fitness_goals' not in st.session_state:
        st.session_state.fitness_goals = {
            'weight': {
                'current': user.get('weight', 70),
                'target': user.get('weight', 70) - 5 if user.get('fitness_goal') == 'Weight Loss' else user.get('weight', 70) + 5,
                'unit': 'kg'
            },
            'calories': {
                'daily': 2200 if user.get('gender') == 'Male' else 1800,
                'burned': 0,
                'unit': 'kcal'
            },
            'workouts': {
                'weekly_target': 4,
                'completed': 0,
                'unit': 'sessions'
            },
            'steps': {
                'daily_target': 10000,
                'current': 0,
                'unit': 'steps'
            }
        }
else:
    # Default goals for non-authenticated users
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
    from pages.auth import app as auth_app
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

# Check authentication
if not st.session_state.authenticated:
    auth_app()
else:
    # Initialize session state for navigation
    if 'nav_selection' not in st.session_state:
        st.session_state.nav_selection = 'Home'

    # Navigation state management
    def navigate_to(page_name):
        st.session_state.nav_selection = page_name
        st.query_params['nav'] = page_name

    # Sidebar with Logo and User Info
    with st.sidebar:
        st.markdown("""
            <div class="zfit-logo">
                <h1 class="zfit-title">ZFIT</h1>
                <div class="zfit-divider"></div>
                <p class="zfit-slogan">Transform Your Life</p>
                <p class="zfit-subtitle">AI-Powered Fitness & Nutrition Coach</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display user info with more details
        if st.session_state.user:
            user = st.session_state.user
            bmi = round(user.get('weight', 70) / ((user.get('height', 170) / 100) ** 2), 1)
            st.markdown(f"""
                <div class="user-profile-card">
                    <div class="user-info-header">
                        <h3>{user['name']}</h3>
                        <p class="user-goal">{user['fitness_goal']}</p>
                    </div>
                    <div class="user-stats">
                        <div class="stat-item">
                            <span class="stat-label">Weight</span>
                            <span class="stat-value">{user['weight']} kg</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Height</span>
                            <span class="stat-value">{user['height']} cm</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">BMI</span>
                            <span class="stat-value">{bmi}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button('🏠 Back to Home', use_container_width=True):
            navigate_to('Home')
            st.rerun()

        # Logout button
        if st.button('🚪 Logout', use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

        # Quick Access Menu based on user's fitness goal
        if st.session_state.user:
            goal = st.session_state.user['fitness_goal']
            st.markdown(f"""
                <div class="sidebar-menu">
                    <div class="menu-section-title">Your Fitness Journey</div>
                    <div class="menu-item">
                        <i>📊</i>
                        <span class="menu-item-text">Progress Dashboard</span>
                    </div>
                    <div class="menu-item">
                        <i>🎯</i>
                        <span class="menu-item-text">{goal}</span>
                    </div>
                    <div class="menu-item">
                        <i>📅</i>
                        <span class="menu-item-text">Activity Level: {user['activity_level']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
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

    # Main Content Area based on navigation
    if st.session_state.nav_selection == "Home":
        # Hero Section with personalized welcome
        user = st.session_state.user
        st.markdown(f"""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Welcome back, {user['name']}!</h1>
                <p class="hero-subtitle">Let's continue your journey towards {user['fitness_goal']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User Stats Dashboard
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <h3>Current Progress</h3>
                <div class="progress-stats">
                    <div class="progress-item">
                        <span class="label">Weight Goal</span>
                        <div class="progress-bar">
                            <div class="progress" style="width: 60%;"></div>
                        </div>
                    </div>
                    <div class="progress-item">
                        <span class="label">Weekly Workouts</span>
                        <div class="progress-bar">
                            <div class="progress" style="width: 75%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <h3>Today's Goals</h3>
                <div class="goal-list">
                    <div class="goal-item">
                        <span class="goal-icon">🏃‍♂️</span>
                        <span class="goal-text">Complete 30min workout</span>
                    </div>
                    <div class="goal-item">
                        <span class="goal-icon">🥗</span>
                        <span class="goal-text">Track meals</span>
                    </div>
                    <div class="goal-item">
                        <span class="goal-icon">💧</span>
                        <span class="goal-text">Drink 8 glasses of water</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card">
                <h3>Weekly Summary</h3>
                <div class="summary-stats">
                    <div class="summary-item">
                        <span class="number">3</span>
                        <span class="label">Workouts</span>
                    </div>
                    <div class="summary-item">
                        <span class="number">1,200</span>
                        <span class="label">Calories Burned</span>
                    </div>
                    <div class="summary-item">
                        <span class="number">25,000</span>
                        <span class="label">Steps</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Rest of the home page content...
        
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



