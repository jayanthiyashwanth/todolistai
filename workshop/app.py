import streamlit as st
from utils.session import init_session
from utils.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="SmartTodoAI - Smart Task Management",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global custom styles (hides default sidebar nav)
apply_custom_css()

# Initialize session
init_session()

# Route based on login state
if st.session_state.get("logged_in", False):
    st.switch_page("pages/dashboard.py")
else:
    st.switch_page("pages/login.py")
