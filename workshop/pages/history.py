import streamlit as st
from datetime import datetime
from utils.session import require_auth
from utils.database import load_json, get_file_path, restore, delete, find_by_username
from utils.styles import apply_custom_css, render_sidebar_menu

# Page configuration
st.set_page_config(
    page_title="SmartTodoAI - History",
    page_icon="assets/logo.png",
    layout="wide"
)

# Apply custom styling (hides default sidebar navigation)
apply_custom_css()

# Enforce auth rule
require_auth()

current_user = st.session_state.user
username = current_user.get("username", "")

# Render custom sidebar navigation
render_sidebar_menu("History")

st.markdown('<h1 class="gradient-header">Task History</h1>', unsafe_allow_html=True)
st.markdown('<p class="gradient-subtext">View and manage your deleted tasks. Restored tasks will appear on the Dashboard.</p>', unsafe_allow_html=True)

# Fetch Todos
all_todos = find_by_username("todos", username)
deleted_todos = [t for t in all_todos if t.get("is_deleted", False)]

if "confirm_delete_id" not in st.session_state:
    st.session_state.confirm_delete_id = None

if not deleted_todos:
    st.info("Your task history is empty! Tasks you delete from the Dashboard will appear here.")
else:
    # Display confirmation dialog at the top if active
    if st.session_state.confirm_delete_id:
        to_delete = next((t for t in deleted_todos if t["id"] == st.session_state.confirm_delete_id), None)
        if to_delete:
            st.warning(f"⚠️ Are you sure you want to permanently delete the task: **'{to_delete.get('title')}'**? This action cannot be undone.")
            col_confirm1, col_confirm2, _ = st.columns([1, 1, 5])
            with col_confirm1:
                if st.button("Yes, Delete Forever", type="primary", use_container_width=True):
                    if delete("todos", to_delete["id"]):
                        st.success("Task permanently deleted.")
                        st.session_state.confirm_delete_id = None
                        st.rerun()
                    else:
                        st.error("Error deleting task.")
            with col_confirm2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_delete_id = None
                    st.rerun()
            st.markdown("<hr/>", unsafe_allow_html=True)

    # Render deleted tasks list
    for todo in deleted_todos:
        tid = todo["id"]
        priority_class = f"priority-{todo.get('priority', 'medium').lower()}"
        created_date = todo.get("created_at", "")[:10] if todo.get("created_at") else "N/A"
        deleted_date = todo.get("deleted_at", "")[:10] if todo.get("deleted_at") else "N/A"
        
        st.markdown(
            f'<div class="todo-card {priority_class}" style="opacity: 0.85;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center;">'
            f'<h4 style="margin: 0; font-size: 1.15rem; color:#d1d5db; text-decoration: line-through;">{todo.get("title")}</h4>'
            f'<span style="font-size:0.8rem; font-weight:600; padding:2px 8px; border-radius:12px; background-color:#374151; color:#9ca3af;">{todo.get("priority")}</span>'
            f'</div>'
            f'<p style="margin: 8px 0; color:#6b7280; font-size:0.9rem;">{todo.get("description", "")}</p>'
            f'<div style="display:flex; gap:20px; font-size:0.8rem; color:#4b5563;">'
            f'<span>📅 Created: {created_date}</span>'
            f'<span>🗑 Deleted: {deleted_date}</span>'
            f'<span>Status: {todo.get("status")}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Action Buttons in columns
        btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 5])
        
        with btn_col1:
            if st.button("Restore ↩", key=f"restore_{tid}"):
                if restore("todos", tid):
                    st.success(f"Task '{todo.get('title')}' restored to Dashboard!")
                    st.rerun()
                else:
                    st.error("Error restoring task.")
                    
        with btn_col2:
            if st.button("Delete Forever 🗑", key=f"perm_delete_{tid}"):
                st.session_state.confirm_delete_id = tid
                st.rerun()
                
        st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)
