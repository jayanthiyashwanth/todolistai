import streamlit as st
from utils.session import require_guest, login_user
from utils.auth import authenticate_user
from utils.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartTodoAI - Login",
    page_icon="assets/logo.png",
    layout="wide"
)

# Apply styling (hides default sidebar navigation)
apply_custom_css()

# Enforce guest rule: if already logged in, redirect to dashboard
require_guest()

# Center Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div style="text-align: center; margin-top: 50px;">', unsafe_allow_html=True)
    # Display logo
    try:
        st.image("assets/logo.png", width=100)
    except Exception:
        pass
    
    st.markdown('<h1 class="gradient-header">SmartTodoAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtext">Manage tasks efficiently with AI power and sleek design.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login card container
    with st.container():
        st.markdown(
            '<div style="background-color: #1f2937; padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.15);">', 
            unsafe_allow_html=True
        )
        
        st.subheader("Login to your Account")
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_username").strip()
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Login action
        if st.button("Login", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                user = authenticate_user(username, password)
                if user:
                    login_user(user)
                else:
                    st.error("Invalid username or password.")
                    
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    if st.button("Don't have an account? Register here", use_container_width=True):
        st.switch_page("pages/register.py")
    st.markdown('</div>', unsafe_allow_html=True)
