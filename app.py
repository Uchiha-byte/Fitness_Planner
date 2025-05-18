"""
Main application file
"""

import streamlit as st
from streamlit_option_menu import option_menu

# Clear cache and session state for fresh reload
st.cache_data.clear()
if not st.session_state.get('app_init'):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.app_init = True

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

# Page config
st.set_page_config(
    page_title="ZFIT AI POWERED FITNESS TRACKER AND PLANNER",
    page_icon="💪",
    layout="wide"
)

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

    # ZFIT Brand Container
    st.markdown("""
        <div class="stats-container">
            <div class="stats-title">ZFIT</div>
            <p class="stats-subtitle">AI-Powered Fitness Tracker and Planner</p>
        </div>
    """, unsafe_allow_html=True)

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
            <p>© 2024 ZFIT. All rights reserved.</p>
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
    # Welcome Section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #e2e8f0; font-size: 3.5em; font-weight: bold;'>Welcome to ZFIT</h1>
        <p style='color: #a0aec0; font-size: 1.5em; margin-bottom: 2rem;'>Your Personal AI Fitness Coach & Nutrition Guide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='#Exercise-Library'" style='cursor: pointer;'>
            <h3 class="feature-title">🏋️‍♂️ Exercise Library</h3>
            <p class="feature-text">Browse our comprehensive collection of exercises with detailed instructions and form guidance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='#Workout-Planner'" style='cursor: pointer;'>
            <h3 class="feature-title">📊 Workout Planner</h3>
            <p class="feature-text">Create and manage personalized workout plans tailored to your goals.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='#Nutrition-Tracker'" style='cursor: pointer;'>
            <h3 class="feature-title">🍎 Nutrition Tracker</h3>
            <p class="feature-text">Track your daily nutrition, monitor macros, and get personalized recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" onclick="window.location.href='#AI-Coach'" style='cursor: pointer;'>
            <h3 class="feature-title">🤖 AI Coach</h3>
            <p class="feature-text">Get real-time guidance and answers to your fitness questions.</p>
        </div>
        """, unsafe_allow_html=True)

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