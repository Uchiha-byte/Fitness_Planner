import streamlit as st
from utils.db_manager import (
    create_user,
    verify_user,
    DatabaseManager,
    reset_database,
    get_user_by_username
)
import logging

# Set up logging - only for errors
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def app():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    if 'auth_error' not in st.session_state:
        st.session_state.auth_error = None
    if 'auth_success' not in st.session_state:
        st.session_state.auth_success = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #1a1f2d;
        color: #ffffff;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {visibility: hidden;}
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 3rem;
        max-width: 300px;
    }
    .logo-icon {
        width: 64px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #4A90E2;
        background: #252b3b;
        border-radius: 12px;
        margin-right: 1.25rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        flex-shrink: 0;
    }
    .logo-text {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .logo-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4A90E2;
        letter-spacing: 1px;
        line-height: 1.2;
        margin-bottom: 0.25rem;
    }
    .logo-tagline {
        font-size: 1rem;
        color: #8b95a9;
        line-height: 1.4;
    }
    
    /* Form header */
    .form-header {
        text-align: center;
        margin-bottom: 2.5rem;
        color: #ffffff;
        font-size: 1.8rem;
        line-height: 1.4;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4A90E2;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #2d3446;
    }
    
    /* Message styling */
    .success-message {
        padding: 1.25rem;
        background-color: rgba(47, 129, 90, 0.1);
        color: #2ecc71;
        border: 1px solid rgba(47, 129, 90, 0.2);
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        animation: fadeIn 0.5s ease-in;
        line-height: 1.4;
    }
    .error-message {
        padding: 1.25rem;
        background-color: rgba(231, 76, 60, 0.1);
        color: #e74c3c;
        border: 1px solid rgba(231, 76, 60, 0.2);
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        animation: fadeIn 0.5s ease-in;
        line-height: 1.4;
    }
    
    /* Button container styling */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Primary button styling */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
    }
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5a9ee8 0%, #4087c9 100%) !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3) !important;
        transform: translateY(-2px);
    }
    .stButton button[kind="primary"]:active {
        transform: translateY(1px) !important;
    }
    
    /* Secondary button styling */
    .stButton button[kind="secondary"] {
        background: #1e2536 !important;
        color: #8b95a9 !important;
        border: 2px solid #2d3446 !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: #252b3b !important;
        color: white !important;
        border-color: #4A90E2 !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15) !important;
        transform: translateY(-2px);
    }
    .stButton button[kind="secondary"]:active {
        transform: translateY(1px) !important;
    }
    
    /* Button text styling */
    .stButton button {
        font-size: 1.1rem !important;
        height: auto !important;
        min-height: 3rem !important;
        white-space: nowrap !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive styling */
    @media (max-width: 768px) {
        .stButton button {
            font-size: 1rem !important;
            padding: 0.625rem 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Logo and branding
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">Z</div>
            <div class="logo-text">
                <span class="logo-title">ZFIT</span>
                <span class="logo-tagline">AI-Powered Fitness</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Display messages
    if st.session_state.auth_success:
        st.markdown(f'<div class="success-message">{st.session_state.auth_success}</div>', unsafe_allow_html=True)
    
    if st.session_state.auth_error:
        st.markdown(f'<div class="error-message">{st.session_state.auth_error}</div>', unsafe_allow_html=True)

    # Auth mode buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", key="login_btn", 
                    help="Switch to login mode",
                    use_container_width=True,
                    type="secondary" if st.session_state.auth_mode != 'login' else "primary"):
            st.session_state.auth_mode = 'login'
            st.session_state.auth_error = None
            st.session_state.auth_success = None
            st.rerun()
            
    with col2:
        if st.button("✨ Sign Up", key="signup_btn",
                    help="Switch to signup mode",
                    use_container_width=True,
                    type="secondary" if st.session_state.auth_mode != 'signup' else "primary"):
            st.session_state.auth_mode = 'signup'
            st.session_state.auth_error = None
            st.session_state.auth_success = None
            st.rerun()

    # Login form
    if st.session_state.auth_mode == 'login':
        st.markdown('<h2 class="form-header">Welcome Back!</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            submit = st.form_submit_button("Login →")
            
            if submit:
                if not username or not password:
                    st.session_state.auth_error = "❌ Please fill in all fields"
                    st.rerun()
                
                success, result = verify_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = result
                    st.session_state.auth_error = None
                    st.session_state.auth_success = "✅ Login successful!"
                    st.rerun()
                else:
                    st.session_state.auth_error = "❌ Invalid username or password"
                    st.rerun()
    
    # Signup form
    else:
        st.markdown('<h2 class="form-header">Create Your Account</h2>', unsafe_allow_html=True)
        
        with st.form("signup_form"):
            # Personal Information Section
            st.markdown('<p class="section-title">Personal Information</p>', unsafe_allow_html=True)
            username = st.text_input("👤 Username", help="Choose a unique username (3-20 characters)")
            name = st.text_input("📛 Full Name")
            email = st.text_input("📧 Email Address (Optional)")
            password = st.text_input("🔒 Password", type="password", help="At least 6 characters")
            password_confirm = st.text_input("🔒 Confirm Password", type="password")

            # Physical Information Section
            st.markdown('<p class="section-title">Physical Information</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                weight = st.number_input("⚖️ Weight (kg)", min_value=30.0, max_value=250.0, value=70.0)
            with col2:
                height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
            with col3:
                age = st.number_input("🎂 Age", min_value=13, max_value=100, value=25)
            
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])

            # Fitness Goals Section
            st.markdown('<p class="section-title">Fitness Goals</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                fitness_goal = st.selectbox("🎯 Goal", [
                    "Weight Loss",
                    "Muscle Gain",
                    "Maintain",
                    "General Fitness"
                ])
            with col2:
                activity_level = st.selectbox("📈 Activity", [
                    "Sedentary",
                    "Light",
                    "Moderate",
                    "Very Active",
                    "Extra Active"
                ])

            # Submit button
            submit = st.form_submit_button("Create Account →")
            
            if submit:
                validation_errors = []
                
                if not username:
                    validation_errors.append("Username is required")
                elif len(username) < 3:
                    validation_errors.append("Username must be at least 3 characters")
                
                if not name:
                    validation_errors.append("Name is required")
                
                if not password:
                    validation_errors.append("Password is required")
                elif len(password) < 6:
                    validation_errors.append("Password must be at least 6 characters")
                
                if password != password_confirm:
                    validation_errors.append("Passwords do not match")
                
                if validation_errors:
                    st.session_state.auth_error = "❌ " + "\n❌ ".join(validation_errors)
                    st.rerun()
                
                try:
                    success, message = create_user(
                        username=username,
                        name=name,
                        password=password,
                        email=email if email else None,
                        weight=weight,
                        height=height,
                        age=age,
                        gender=gender,
                        fitness_goal=fitness_goal,
                        activity_level=activity_level
                    )
                    
                    if success:
                        user_check = get_user_by_username(username)
                        if not user_check:
                            st.session_state.auth_error = "❌ Signup failed: user not found after creation. Please try again."
                            st.rerun()
                        st.session_state.auth_success = f"✅ {message}\nPlease log in with your new account."
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.session_state.auth_error = f"❌ {message}"
                        st.rerun()
                        
                except Exception as e:
                    st.session_state.auth_error = f"❌ An error occurred: {str(e)}"
                    st.rerun() 