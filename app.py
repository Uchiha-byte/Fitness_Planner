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
    get_db,
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
        conn = get_db()
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

    # Custom CSS for the entire app
    st.markdown("""
        <style>
            /* Main Logo Styles */
            .main-logo {
                text-align: center;
                margin: 2rem 0;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            
            .logo-icon {
                font-family: 'Stencil', 'Arial Black', sans-serif;
                font-size: 8rem;
                font-weight: 900;
                color: #0066CC;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                background: linear-gradient(135deg, #0066CC, #0099FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                padding: 20px;
                border-radius: 20px;
                background-color: rgba(0, 102, 204, 0.1);
                box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
                animation: float 3s ease-in-out infinite;
            }
            
            .logo-text {
                font-family: 'Stencil', 'Arial Black', sans-serif;
                font-size: 4rem;
                font-weight: 900;
                color: #0066CC;
                margin: 1rem 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                background: linear-gradient(135deg, #0066CC, #0099FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .logo-tagline {
                font-size: 1.5rem;
                color: #666;
                margin: 0.5rem 0;
                font-weight: 500;
            }
            
            /* Sidebar Logo Styles */
            .sidebar-logo {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 20px 0;
                margin-bottom: 20px;
                width: 100%;
                text-align: center;
            }
            
            .sidebar-logo .logo-icon {
                width: 90px;
                height: 90px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Stencil', 'Arial Black', sans-serif;
                font-size: 3.5rem;
                font-weight: 900;
                color: #0066CC;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                background: linear-gradient(135deg, #0066CC, #0099FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                border-radius: 20px;
                background-color: rgba(0, 102, 204, 0.12);
                box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
                animation: float 3s ease-in-out infinite;
                margin: 0 auto;
                text-align: center;
            }
            
            .sidebar-logo .logo-text {
                font-family: 'Stencil', 'Arial Black', sans-serif;
                font-size: 1.5rem;
                font-weight: 900;
                color: #0066CC;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                background: linear-gradient(135deg, #0066CC, #0099FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
            }
            
            .sidebar-logo .logo-tagline {
                font-size: 1rem;
                color: #666;
                margin: 0;
                font-weight: 500;
                text-align: center;
            }
            
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-5px); }
                100% { transform: translateY(0px); }
            }
            
            /* Rest of your existing styles */
            // ... existing code ...
        </style>
    """, unsafe_allow_html=True)

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
                <div class="sidebar-logo">
                    <div class="logo-icon">Z</div>
                    <div class="logo-text">
                        <h1 class="logo-title">ZFIT</h1>
                        <p class="logo-tagline">AI-Powered Fitness</p>
                    </div>
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
            # Hero Section
            st.markdown(f"""
            <div class="hero-section" style="background-image: url('https://img.pikbest.com/origin/10/04/67/06tpIkbEsTUP5.jpg!w700wp');">
                <div class="hero-overlay"></div>
                <div class="hero-content">
                    <div class="hero-text">
                        <h1 class="hero-title">Welcome back, {st.session_state.user['name']}!</h1>
                        <p class="hero-subtitle">Let's continue your journey towards {st.session_state.user['fitness_goal']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Access Section
            st.header("Quick Access")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <div class="feature-card" style="background-image: url('https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=400&q=80');">
                        <div class="feature-content">
                            <h3>📝 Plan Workout</h3>
                            <p>Create your personalized workout plan</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Plan Workout", use_container_width=True):
                    navigate_to("Workout Planner")
                    
            with col2:
                st.markdown("""
                    <div class="feature-card" style="background-image: url('https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=400&q=80');">
                        <div class="feature-content">
                            <h3>🍎 Log Nutrition</h3>
                            <p>Track your daily nutrition intake</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Log Nutrition", use_container_width=True):
                    navigate_to("Nutrition Tracker")
                    
            with col3:
                st.markdown("""
                    <div class="feature-card" style="background-image: url('https://stayfitcentral.com/wp-content/uploads/2024/08/Endura-Best-AI-Personal-Trainer-1400x800.webp');">
                        <div class="feature-content">
                            <h3>🤖 AI Coach</h3>
                            <p>Get personalized fitness guidance</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("AI Coach", use_container_width=True):
                    navigate_to("AI Coach")

            # Motivation Section
            st.markdown("""
                <div class="motivation-section">
                    <div class="motivation-header">
                        <h2>Daily Motivation</h2>
                        <p class="motivation-subtitle">Stay inspired on your fitness journey</p>
                    </div>
                    <div class="quotes-grid">
                        <div class="quote-card" style="background-image: url('https://img.freepik.com/premium-vector/only-bad-workout-is-one-that-didnt-happen-inspiring-workout-gym-motivation-quote-illustrat_1085864-300.jpg');">
                            <div class="quote-overlay"></div>
                            <div class="quote-content">
                                <p class="quote">"The only Bad Workout is one that didnt happen."</p>
                            </div>
                        </div>
                        <div class="quote-card" style="background-image: url('https://pbs.twimg.com/media/EGA0itTWsAAtMK6.jpg');">
                            <div class="quote-overlay"></div>
                            <div class="quote-content">
                                <p class="quote">"Your body can stand almost anything. It's your mind you have to convince."</p>
                            </div>
                        </div>
                        <div class="quote-card" style="background-image: url('https://m.media-amazon.com/images/I/51sbnUqevKL._AC_.jpg');">
                            <div class="quote-overlay"></div>
                            <div class="quote-content">
                                <p class="quote">"BELIEVE  DISCIPLINE  STRONG  CONSISTENCY SECRET"</p>
                            </div>
                        </div>
                    </div>
                    <div class="motivation-footer">
                        <div class="motivation-tip">
                            <div class="tip-icon">💡</div>
                            <p>Let these powerful images inspire your workout today!</p>
                        </div>
                        <div class="motivation-stats">
                            <div class="stat-item">
                                <span class="stat-number">7</span>
                                <span class="stat-label">Days of Consistency</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">21</span>
                                <span class="stat-label">Days to Form a Habit</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">90</span>
                                <span class="stat-label">Days to Transform</span>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Update CSS for the motivation section
            st.markdown("""
                <style>
                    .motivation-section {
                        margin: 4rem 0;
                        padding: 3rem;
                        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
                        border-radius: 20px;
                        border: 1px solid rgba(76, 154, 255, 0.2);
                        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    }
                    .motivation-header {
                        text-align: center;
                        margin-bottom: 3rem;
                    }
                    .motivation-header h2 {
                        color: #4c9aff;
                        font-size: 2.5rem;
                        font-weight: 700;
                        margin-bottom: 0.5rem;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                    }
                    .motivation-subtitle {
                        color: #CCCCCC;
                        font-size: 1.2rem;
                        font-style: italic;
                    }
                    .quotes-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 2rem;
                        margin: 2rem 0;
                    }
                    .quote-card {
                        position: relative;
                        height: 400px;
                        background-size: cover;
                        background-position: center;
                        border-radius: 15px;
                        overflow: hidden;
                        transition: all 0.3s ease;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                    }
                    .quote-card:hover {
                        transform: translateY(-10px) scale(1.02);
                        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                    }
                    .quote-overlay {
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%);
                        transition: all 0.3s ease;
                    }
                    .quote-card:hover .quote-overlay {
                        background: linear-gradient(135deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.2) 100%);
                    }
                    .quote-content {
                        position: relative;
                        z-index: 1;
                        padding: 2rem;
                        height: 100%;
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-end;
                        color: white;
                        text-align: center;
                        transform: translateY(0);
                        transition: all 0.3s ease;
                    }
                    .quote-card:hover .quote-content {
                        transform: translateY(-10px);
                    }
                    .quote {
                        font-style: italic;
                        font-size: 1.5rem;
                        line-height: 1.6;
                        color: #FFFFFF;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                        font-weight: 600;
                        margin: 0;
                        padding: 1rem;
                        background: rgba(0,0,0,0.3);
                        border-radius: 10px;
                        backdrop-filter: blur(5px);
                    }
                    .motivation-footer {
                        margin-top: 3rem;
                        padding-top: 2rem;
                        border-top: 1px solid rgba(76, 154, 255, 0.2);
                    }
                    .motivation-tip {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 1rem;
                        background: rgba(76, 154, 255, 0.1);
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin-bottom: 2rem;
                    }
                    .tip-icon {
                        font-size: 2rem;
                        color: #4c9aff;
                    }
                    .motivation-tip p {
                        color: #CCCCCC;
                        font-size: 1.1rem;
                        font-style: italic;
                        margin: 0;
                    }
                    .motivation-stats {
                        display: flex;
                        justify-content: space-around;
                        gap: 2rem;
                        margin-top: 2rem;
                    }
                    .stat-item {
                        text-align: center;
                        padding: 1.5rem;
                        background: rgba(255,255,255,0.05);
                        border-radius: 10px;
                        transition: transform 0.3s ease;
                    }
                    .stat-item:hover {
                        transform: translateY(-5px);
                        background: rgba(255,255,255,0.08);
                    }
                    .stat-number {
                        display: block;
                        font-size: 2.5rem;
                        font-weight: 700;
                        color: #4c9aff;
                        margin-bottom: 0.5rem;
                    }
                    .stat-label {
                        color: #CCCCCC;
                        font-size: 1rem;
                    }

                    @media (max-width: 768px) {
                        .motivation-section {
                            padding: 2rem;
                            margin: 2rem 0;
                        }
                        .motivation-header h2 {
                            font-size: 2rem;
                        }
                        .quotes-grid {
                            grid-template-columns: 1fr;
                        }
                        .quote-card {
                            height: 300px;
                        }
                        .quote {
                            font-size: 1.2rem;
                        }
                        .motivation-stats {
                            flex-direction: column;
                            gap: 1rem;
                        }
                        .stat-item {
                            width: 100%;
                        }
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



