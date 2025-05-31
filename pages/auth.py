import streamlit as st
from utils.db_manager import create_user, verify_user, DatabaseManager

def app():
    # Initialize database
    db_manager = DatabaseManager()
    
    # Hide Streamlit's default menu and footer
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Auth container with glass morphism effect
    st.markdown("""
        <div class="auth-container">
            <div class="auth-box">
                <div class="auth-header">
                    <div class="logo-container">
                        <div class="logo-icon">Z</div>
                        <div class="logo-text">
                            <span class="logo-title">ZFIT</span>
                            <span class="logo-tagline">AI-Powered Fitness</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for auth mode
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'

    col1, col2 = st.columns(2)
    with col1:
        if st.button('🔑 Login', use_container_width=True, 
                     type='primary' if st.session_state.auth_mode == 'login' else 'secondary',
                     key='login_toggle'):
            st.session_state.auth_mode = 'login'
    with col2:
        if st.button('✨ Sign Up', use_container_width=True,
                     type='primary' if st.session_state.auth_mode == 'signup' else 'secondary',
                     key='signup_toggle'):
            st.session_state.auth_mode = 'signup'
    st.markdown('</div>', unsafe_allow_html=True)

    
    if st.session_state.auth_mode == 'login':
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<h2 class="form-title">Login to Your Account</h2>', unsafe_allow_html=True)
            
            identifier = st.text_input("👤 Username or Email",
                                     help="Enter your username or email address")
            password = st.text_input("🔒 Password", type="password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Login →", use_container_width=True)

            if submit:
                if identifier and password:
                    try:
                        success, result = verify_user(identifier, password)
                        if success:
                            st.session_state.user = result
                            st.session_state.authenticated = True
                            st.rerun()
                        else:
                            st.error("❌ " + result)
                    except Exception as e:
                        st.error(f"❌ An error occurred during login: {str(e)}")
                else:
                    st.error("❌ Please fill in all fields")

    else:  # Signup mode
        with st.form("signup_form", clear_on_submit=True):
            st.markdown('<h2 class="form-title">Create Your Account</h2>', unsafe_allow_html=True)
            
            # Personal Information
            st.markdown('<p class="form-section-title">Personal Information</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("👤 Username", 
                                       help="Choose a unique username (3-20 characters, letters, numbers, - and _)")
                name = st.text_input("📛 Full Name")
            with col2:
                email = st.text_input("📧 Email Address")
                password = st.text_input("🔒 Password", type="password", 
                                       help="Password must be at least 6 characters long")
                confirm_password = st.text_input("🔒 Confirm Password", type="password")
            
            # Physical Information
            st.markdown('<p class="form-section-title">Physical Information</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                weight = st.number_input("⚖️ Weight (kg)", 
                                       min_value=20.0, max_value=300.0, value=70.0,
                                       help="Enter your current weight in kilograms")
            with col2:
                height = st.number_input("📏 Height (cm)", 
                                       min_value=100.0, max_value=250.0, value=170.0,
                                       help="Enter your height in centimeters")
            with col3:
                age = st.number_input("🎂 Age", 
                                    min_value=13, max_value=100, value=25,
                                    help="Enter your age in years")
            
            col1, col2 = st.columns(2)
            with col1:
                gender = st.selectbox("⚧ Gender", 
                                    ["Select Gender", "Male", "Female", "Other"],
                                    index=0)
            
            # Fitness Goals
            st.markdown('<p class="form-section-title">Fitness Goals</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                fitness_goal = st.selectbox("🎯 Fitness Goal", [
                    "Select Goal",
                    "Weight Loss",
                    "Muscle Gain",
                    "Maintain Weight",
                    "Improve Fitness",
                    "Build Strength"
                ], index=0)
            
            with col2:
                activity_level = st.selectbox("📈 Activity Level", [
                    "Select Activity Level",
                    "Sedentary",
                    "Lightly Active",
                    "Moderately Active",
                    "Very Active",
                    "Extremely Active"
                ], index=0)

            # Center the submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Create Account →", use_container_width=True)

            if submit:
                if not all([username, name, email, password, confirm_password]):
                    st.error("❌ Please fill in all required fields")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                elif gender == "Select Gender":
                    st.error("❌ Please select your gender")
                elif fitness_goal == "Select Goal":
                    st.error("❌ Please select your fitness goal")
                elif activity_level == "Select Activity Level":
                    st.error("❌ Please select your activity level")
                else:
                    success, message = create_user(
                        username=username,
                        name=name,
                        email=email,
                        password=password,
                        weight=weight,
                        height=height,
                        age=age,
                        gender=gender,
                        fitness_goal=fitness_goal,
                        activity_level=activity_level
                    )
                    if success:
                        st.success("✅ " + message)
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.error("❌ " + message)
    
    st.markdown('</div>', unsafe_allow_html=True) 