"""
Main application file
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime, timedelta
from utils.db_manager import (
    get_user_by_id, 
    update_user_profile, 
    DatabaseManager,
    get_db_connection,
    verify_user,
    create_user
)
import plotly.express as px
import config
import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_user_summary(user_id):
    """Get summary of user's fitness data"""
    try:
        # Get user profile
        user_data = get_user_by_id(user_id)
        if not user_data:
            return None
        
        # Get recent workout logs
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get workout logs
        cursor.execute('''
            SELECT * FROM workout_logs 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT 5
        ''', (user_id,))
        workout_logs = [dict(row) for row in cursor.fetchall()]
        
        # Get nutrition logs
        cursor.execute('''
            SELECT * FROM nutrition_logs 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT 5
        ''', (user_id,))
        nutrition_logs = [dict(row) for row in cursor.fetchall()]
        
        # Get progress tracking data
        cursor.execute('''
            SELECT * FROM progress_tracking 
            WHERE user_id = ? 
            ORDER BY date DESC
        ''', (user_id,))
        progress_data = [dict(row) for row in cursor.fetchall()]
        
        # Get current daily goals
        cursor.execute('''
            SELECT * FROM daily_goals 
            WHERE user_id = ? 
            ORDER BY date_modified DESC 
            LIMIT 1
        ''', (user_id,))
        current_goals = cursor.fetchone()
        
        conn.close()
        
        return {
            'user_data': user_data,
            'workout_logs': workout_logs,
            'nutrition_logs': nutrition_logs,
            'progress_data': progress_data,
            'current_goals': dict(current_goals) if current_goals else None
        }
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        return None

def create_progress_chart(progress_data):
    """Create a progress tracking chart"""
    if not progress_data:
        return None
        
    df = pd.DataFrame(progress_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create multiple traces for different metrics
    fig = px.line(df, x='date', y=['weight', 'body_fat', 'muscle_mass'],
                  title='Progress Tracking',
                  labels={
                      'weight': 'Weight (kg)',
                      'body_fat': 'Body Fat (%)',
                      'muscle_mass': 'Muscle Mass (kg)',
                      'date': 'Date'
                  })
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        showlegend=True,
        legend_title="Metrics"
    )
    return fig

def main():
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

    # Initialize session state for data refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    # Add auto-refresh every 30 seconds
    if (datetime.now() - st.session_state.last_refresh).seconds > 30:
        st.session_state.last_refresh = datetime.now()
        st.rerun()

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
            st.markdown(f"""
            <div class="hero-section">
                <div class="hero-content">
                    <h1 class="hero-title">Welcome back, {st.session_state.user['name']}!</h1>
                    <p class="hero-subtitle">Let's continue your journey towards {st.session_state.user['fitness_goal']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Access Section
            st.header("Quick Access")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📝 Plan Workout", use_container_width=True):
                    navigate_to("Workout Planner")
                    
            with col2:
                if st.button("🍎 Log Nutrition", use_container_width=True):
                    navigate_to("Nutrition Tracker")
                    
            with col3:
                if st.button("📊 Track Progress", use_container_width=True):
                    navigate_to("Progress Tracking")
            
            # About ZFIT Section
            st.markdown("""
                <div class="about-section">
                    <h2>About ZFIT</h2>
                    <p class="about-subtitle">Your AI-Powered Fitness Journey Companion</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Features Grid
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div class="feature-card">
                        <h3>🎯 Smart Workout Planning</h3>
                        <p>Personalized workout plans tailored to your goals, fitness level, and preferences. 
                        Our AI analyzes your progress and adjusts your routine for optimal results.</p>
                    </div>
                    
                    <div class="feature-card">
                        <h3>🍎 Intelligent Nutrition Tracking</h3>
                        <p>Track your meals, monitor macros, and get personalized nutrition recommendations. 
                        Our AI helps you make informed food choices aligned with your fitness goals.</p>
                    </div>
                    
                    <div class="feature-card">
                        <h3>📊 Comprehensive Progress Tracking</h3>
                        <p>Monitor your weight, body composition, and workout performance over time. 
                        Visualize your progress with detailed charts and analytics.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div class="feature-card">
                        <h3>🤖 AI Coach</h3>
                        <p>Get instant answers to your fitness questions, form checks, and personalized advice. 
                        Your virtual fitness coach is available 24/7 to guide your journey.</p>
                    </div>
                    
                    <div class="feature-card">
                        <h3>📸 Food Vision</h3>
                        <p>Simply take a photo of your meal to get instant nutritional information. 
                        Our AI-powered food recognition makes tracking effortless.</p>
                    </div>
                    
                    <div class="feature-card">
                        <h3>💪 Exercise Library</h3>
                        <p>Access a comprehensive database of exercises with detailed instructions, 
                        form videos, and expert tips to ensure proper technique.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Motivational Quotes
            st.markdown("""
                <div class="motivation-section">
                    <h3>Daily Motivation</h3>
                    <div class="quote-card">
                        <p class="quote">"The only bad workout is the one that didn't happen."</p>
                        <p class="quote-author">- Unknown</p>
                    </div>
                    <div class="quote-card">
                        <p class="quote">"Your body can stand almost anything. It's your mind you have to convince."</p>
                        <p class="quote-author">- Andrew Murphy</p>
                    </div>
                    <div class="quote-card">
                        <p class="quote">"The difference between the impossible and the possible lies in a person's determination."</p>
                        <p class="quote-author">- Tommy Lasorda</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add CSS for the new sections
            st.markdown("""
                <style>
                    .about-section {
                        text-align: center;
                        margin: 2rem 0;
                        padding: 2rem;
                        background: #1E1E1E;
                        border-radius: 15px;
                        color: #FFFFFF;
                        border: 1px solid rgba(76, 154, 255, 0.2);
                    }
                    .about-subtitle {
                        color: #A0A0A0;
                        font-size: 1.2rem;
                        margin-top: 0.5rem;
                    }
                    .feature-card {
                        background: #2D2D2D;
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                        color: #FFFFFF;
                        border: 1px solid #3D3D3D;
                        transition: transform 0.2s ease;
                    }
                    .feature-card:hover {
                        transform: translateY(-5px);
                        border-color: rgba(76, 154, 255, 0.3);
                    }
                    .feature-card h3 {
                        color: #4c9aff;
                        margin-bottom: 0.5rem;
                        font-size: 1.3rem;
                    }
                    .feature-card p {
                        color: #CCCCCC;
                        line-height: 1.6;
                    }
                    .motivation-section {
                        margin: 2rem 0;
                        padding: 2rem;
                        background: #1E1E1E;
                        border-radius: 15px;
                        border: 1px solid rgba(76, 154, 255, 0.2);
                    }
                    .motivation-section h3 {
                        color: #FFFFFF;
                        text-align: center;
                        margin-bottom: 1.5rem;
                        font-size: 1.4rem;
                    }
                    .quote-card {
                        background: #2D2D2D;
                        border-left: 4px solid #4c9aff;
                        padding: 1.5rem;
                        margin: 1rem 0;
                        border-radius: 0 10px 10px 0;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                        transition: transform 0.2s ease;
                    }
                    .quote-card:hover {
                        transform: translateX(5px);
                        background: #333333;
                    }
                    .quote {
                        font-style: italic;
                        font-size: 1.1rem;
                        color: #FFFFFF;
                        margin-bottom: 0.5rem;
                        line-height: 1.6;
                    }
                    .quote-author {
                        text-align: right;
                        color: #4c9aff;
                        font-size: 0.9rem;
                        font-weight: 500;
                    }
                </style>
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

if __name__ == "__main__":
    main()



