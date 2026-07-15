import streamlit as st

def apply_custom_css():
    """Injects custom CSS to style the application and hide default Streamlit components."""
    css = """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header, Footer and Deploy Button */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    
    /* Hide default Streamlit sidebar multi-page navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Custom background & spacing */
    .stApp {
        background-color: #111827;
        color: #F9FAFB;
    }
    
    /* Gradient Text & Header */
    .gradient-header {
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .gradient-subtext {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Rounded Cards with Glassmorphism and Shadows */
    .stat-card {
        background: #1f2937;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 5px;
        color: #6366f1;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #9ca3af;
        font-weight: 500;
    }
    
    /* Todo Cards styling */
    .todo-card {
        background: #1f2937;
        border-radius: 12px;
        border-left: 6px solid #6b7280; /* Default border color */
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .todo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Priority colored borders */
    .priority-high {
        border-left-color: #ef4444 !important; /* Red */
    }
    .priority-medium {
        border-left-color: #f59e0b !important; /* Amber */
    }
    .priority-low {
        border-left-color: #10b981 !important; /* Emerald */
    }
    
    /* Button custom hover styling */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        border-color: #8b5cf6 !important;
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.25) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #111827;
    }
    ::-webkit-scrollbar-thumb {
        background: #374151;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4b5563;
    }
    
    /* Profile styles */
    .profile-card {
        background: #1f2937;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }
    .profile-item {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .profile-item:last-child {
        border-bottom: none;
    }
    .profile-key {
        font-weight: 500;
        color: #9ca3af;
    }
    .profile-val {
        font-weight: 600;
        color: #f3f4f6;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_sidebar_menu(current_page: str):
    """Renders the custom sidebar navigation menu and handles redirection logic."""
    from streamlit_option_menu import option_menu
    from utils.session import logout_user
    
    # Define our pages map
    pages_list = ["Dashboard", "History", "Profile", "Logout"]
    icons_list = ["house", "clock-history", "person", "box-arrow-right"]
    
    # Determine the selected index based on current_page
    try:
        default_idx = pages_list.index(current_page)
    except ValueError:
        default_idx = 0
        
    with st.sidebar:
        st.markdown(
            '<div style="text-align: center; margin-bottom: 20px;">'
            '<h2 style="font-weight: 800; font-size: 1.5rem; background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">'
            'SmartTodoAI</h2>'
            '<hr style="border-color: rgba(255, 255, 255, 0.05); margin-top: 10px; margin-bottom: 10px;"/>'
            '</div>',
            unsafe_allow_html=True
        )
        
        selected = option_menu(
            menu_title=None,
            options=pages_list,
            icons=icons_list,
            menu_icon="cast",
            default_index=default_idx,
            styles={
                "container": {"padding": "5px", "background-color": "#1f2937", "border-radius": "10px"},
                "icon": {"color": "#a78bfa", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#374151",
                    "color": "#F9FAFB",
                    "border-radius": "8px",
                },
                "nav-link-selected": {"background-color": "#6366f1", "color": "#ffffff"},
            }
        )
        
    # Handle routing based on selection
    if selected != current_page:
        if selected == "Dashboard":
            st.switch_page("pages/dashboard.py")
        elif selected == "History":
            st.switch_page("pages/history.py")
        elif selected == "Profile":
            st.switch_page("pages/profile.py")
        elif selected == "Logout":
            logout_user()
