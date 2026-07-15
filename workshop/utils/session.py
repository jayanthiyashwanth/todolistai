import streamlit as st
from typing import Dict, Any, Optional

def init_session():
    """Initializes standard session state variables if they do not exist."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None

def login_user(user_data: Dict[str, Any]):
    """Sets session state variables for the logged-in user and redirects to Dashboard."""
    st.session_state.logged_in = True
    st.session_state.user = user_data
    st.switch_page("pages/dashboard.py")

def logout_user():
    """Clears authentication session state variables and redirects to Login."""
    st.session_state.logged_in = False
    st.session_state.user = None
    # We clear cache or session state to be fully secure
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Re-initialize basic states
    init_session()
    st.switch_page("pages/login.py")

def require_auth():
    """Ensures user is logged in. If not, redirects to the Login page."""
    init_session()
    if not st.session_state.logged_in:
        st.switch_page("pages/login.py")
        st.stop()

def require_guest():
    """Ensures user is NOT logged in. If they are, redirects to the Dashboard page."""
    init_session()
    if st.session_state.logged_in:
        st.switch_page("pages/dashboard.py")
        st.stop()
