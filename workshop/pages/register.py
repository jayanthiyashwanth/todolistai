import streamlit as st
import time
from utils.session import require_guest
from utils.auth import register_user
from utils.validation import (
    validate_email,
    validate_password_strength,
    is_username_unique,
    is_email_unique
)
from utils.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartTodoAI - Register",
    page_icon="assets/logo.png",
    layout="wide"
)

# Apply custom styling (hides default sidebar navigation)
apply_custom_css()

# Enforce guest rule
require_guest()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div style="text-align: center; margin-top: 30px;">', unsafe_allow_html=True)
    # Display logo
    try:
        st.image("assets/logo.png", width=80)
    except Exception:
        pass
    
    st.markdown('<h1 class="gradient-header">Create an Account</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtext">Join SmartTodoAI to organize your daily activities.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Registration card container
    with st.container():
        st.markdown(
            '<div style="background-color: #1f2937; padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.15);">', 
            unsafe_allow_html=True
        )
        
        fullname = st.text_input("Full Name", placeholder="e.g. John Doe", key="reg_fullname").strip()
        username = st.text_input("Username", placeholder="e.g. johndoe", key="reg_username").strip()
        email = st.text_input("Email Address", placeholder="e.g. john@example.com", key="reg_email").strip()
        password = st.text_input("Password", type="password", placeholder="Create a strong password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", key="reg_confirm_password")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("Register", use_container_width=True, type="primary"):
            # Check required fields
            if not fullname or not username or not email or not password or not confirm_password:
                st.error("All fields are required.")
            # Check password match
            elif password != confirm_password:
                st.error("Passwords do not match.")
            # Validate email
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            # Validate password strength
            else:
                is_strong, msg = validate_password_strength(password)
                if not is_strong:
                    st.error(msg)
                # Check uniqueness
                elif not is_username_unique(username):
                    st.error("Username is already taken. Please choose another.")
                elif not is_email_unique(email):
                    st.error("Email address is already registered. Please choose another.")
                else:
                    # Successful checks, run registration
                    success = register_user(fullname, username, email, password)
                    if success:
                        st.success("Registration successful! Redirecting to login...")
                        time.sleep(1.5)
                        st.switch_page("pages/login.py")
                    else:
                        st.error("An error occurred while saving your details. Please try again.")
                        
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    if st.button("Already have an account? Login here", use_container_width=True):
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)
