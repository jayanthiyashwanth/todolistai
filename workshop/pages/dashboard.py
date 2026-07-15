import streamlit as st
import uuid
from datetime import datetime, date
from utils.session import require_auth
from utils.database import load_json, get_file_path, insert, update, find_by_username
from utils.styles import apply_custom_css, render_sidebar_menu

# Page configuration
st.set_page_config(
    page_title="SmartTodoAI - Dashboard",
    page_icon="assets/logo.png",
    layout="wide"
)

# Apply custom styling (hides default sidebar navigation)
apply_custom_css()

# Enforce auth rule: redirects if not logged in
require_auth()

# Load current user from session
current_user = st.session_state.user
username = current_user.get("username", "")
fullname = current_user.get("fullname", "")

# Render custom sidebar
render_sidebar_menu("Dashboard")

# Main Page Layout
# Header Section
col_header, col_actions = st.columns([2, 1])
with col_header:
    st.markdown(f'<h1 class="gradient-header">Welcome, {fullname}!</h1>', unsafe_allow_html=True)
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f'<div class="gradient-subtext">📅 {today_str}</div>', unsafe_allow_html=True)

with col_actions:
    st.markdown('<div style="text-align: right; padding-top: 15px;">', unsafe_allow_html=True)
    # Quick Navigation buttons
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    with sub_col1:
        if st.button("📁 History", use_container_width=True):
            st.switch_page("pages/history.py")
    with sub_col2:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
    with sub_col3:
        if st.button("🚪 Logout", use_container_width=True):
            from utils.session import logout_user
            logout_user()
    st.markdown('</div>', unsafe_allow_html=True)

# Fetch Todos
all_todos = find_by_username("todos", username)
# Filter out deleted todos
todos = [t for t in all_todos if not t.get("is_deleted", False)]

# Calculate Stats
total_tasks = len(todos)
completed_tasks = len([t for t in todos if t.get("status") == "Completed"])
pending_tasks = total_tasks - completed_tasks
completion_pct = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

# Stats Cards
st.markdown("### Today's Progress")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Total Tasks</div>'
        f'<div class="stat-number">{total_tasks}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
with stat_col2:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Pending Tasks</div>'
        f'<div class="stat-number" style="color: #f59e0b;">{pending_tasks}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
with stat_col3:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Completed Tasks</div>'
        f'<div class="stat-number" style="color: #10b981;">{completed_tasks}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
with stat_col4:
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-label">Completion %</div>'
        f'<div class="stat-number" style="color: #a78bfa;">{completion_pct}%</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# Add Task form inside an expander or container
if "add_task_expanded" not in st.session_state:
    st.session_state.add_task_expanded = False

with st.expander("➕ Add New Todo Task", expanded=st.session_state.add_task_expanded):
    with st.form("add_todo_form", clear_on_submit=True):
        title = st.text_input("Task Title *", placeholder="What needs to be done?")
        description = st.text_area("Description", placeholder="Enter details about this task")
        
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            priority = st.selectbox("Priority Level", ["Low", "Medium", "High"], index=1)
        with form_col2:
            due_date = st.date_input("Due Date", min_value=date.today())
            
        submitted = st.form_submit_button("Add Task", use_container_width=True)
        if submitted:
            if not title.strip():
                st.error("Task Title is required!")
            else:
                new_todo = {
                    "id": str(uuid.uuid4()),
                    "title": title.strip(),
                    "description": description.strip(),
                    "priority": priority,
                    "due_date": due_date.isoformat(),
                    "status": "Pending",
                    "created_at": datetime.now().isoformat(),
                    "completed_at": None,
                    "deleted_at": None,
                    "is_deleted": False,
                    "owner": username
                }
                if insert("todos", new_todo):
                    st.success(f"Task '{title}' added successfully!")
                    st.session_state.add_task_expanded = False
                    st.rerun()
                else:
                    st.error("Failed to add task. Please check permissions.")

st.markdown("<br/>", unsafe_allow_html=True)

# Edit form panel (Active only when editing_todo_id matches)
if "editing_todo_id" not in st.session_state:
    st.session_state.editing_todo_id = None

if st.session_state.editing_todo_id:
    editing_todo = next((t for t in todos if t["id"] == st.session_state.editing_todo_id), None)
    if editing_todo:
        st.markdown("### 📝 Edit Task")
        with st.form("edit_todo_form"):
            edit_title = st.text_input("Task Title", value=editing_todo.get("title", ""))
            edit_description = st.text_area("Description", value=editing_todo.get("description", ""))
            
            edit_col1, edit_col2 = st.columns(2)
            with edit_col1:
                edit_priority = st.selectbox("Priority Level", ["Low", "Medium", "High"], 
                                             index=["Low", "Medium", "High"].index(editing_todo.get("priority", "Medium")))
            with edit_col2:
                # Parse due date safely
                try:
                    default_date = date.fromisoformat(editing_todo.get("due_date", ""))
                except Exception:
                    default_date = date.today()
                edit_due_date = st.date_input("Due Date", value=default_date)
            
            edit_sub_col1, edit_sub_col2 = st.columns(2)
            with edit_sub_col1:
                save_changes = st.form_submit_button("Save Changes", use_container_width=True)
            with edit_sub_col2:
                cancel_changes = st.form_submit_button("Cancel", use_container_width=True)
                
            if save_changes:
                if not edit_title.strip():
                    st.error("Title cannot be empty!")
                else:
                    updated_data = {
                        "title": edit_title.strip(),
                        "description": edit_description.strip(),
                        "priority": edit_priority,
                        "due_date": edit_due_date.isoformat()
                    }
                    if update("todos", editing_todo["id"], updated_data):
                        st.success("Task updated!")
                        st.session_state.editing_todo_id = None
                        st.rerun()
                    else:
                        st.error("Error updating task.")
            elif cancel_changes:
                st.session_state.editing_todo_id = None
                st.rerun()

st.markdown("---")

# Todo List Section with Filters
list_header, search_col, filter_col = st.columns([2, 1, 1])

with list_header:
    st.markdown("### My Tasks")

with search_col:
    search_query = st.text_input("🔍 Search tasks", placeholder="Type title to search...").strip().lower()

with filter_col:
    priority_filter = st.selectbox("Filter Priority", ["All", "High", "Medium", "Low"])

# Apply filters
filtered_todos = todos
if priority_filter != "All":
    filtered_todos = [t for t in filtered_todos if t.get("priority") == priority_filter]
if search_query:
    filtered_todos = [t for t in filtered_todos if search_query in t.get("title", "").lower() or search_query in t.get("description", "").lower()]

# Sort: Pending first, then by priority High -> Low, then by due date
priority_weight = {"High": 0, "Medium": 1, "Low": 2}
filtered_todos.sort(key=lambda t: (
    0 if t.get("status") == "Pending" else 1,
    priority_weight.get(t.get("priority", "Medium"), 1),
    t.get("due_date", "")
))

if not filtered_todos:
    st.info("No tasks found matching your filters. Create a task above to get started!")
else:
    for todo in filtered_todos:
        tid = todo["id"]
        priority_class = f"priority-{todo.get('priority', 'medium').lower()}"
        status_badge = "⏳ Pending" if todo.get("status") == "Pending" else "✅ Completed"
        due_date_val = todo.get("due_date", "No due date")
        
        # Display the custom card using raw html & Streamlit widgets inside it
        # Because we can't capture Streamlit click events inside raw html blocks,
        # we will use an outer container and display status inline using columns.
        
        st.markdown(
            f'<div class="todo-card {priority_class}">'
            f'<div style="display:flex; justify-content:space-between; align-items:center;">'
            f'<h4 style="margin: 0; font-size: 1.15rem; color:#f3f4f6;">{todo.get("title")}</h4>'
            f'<span style="font-size:0.8rem; font-weight:600; padding:2px 8px; border-radius:12px; background-color:#374151; color:#a5b4fc;">{todo.get("priority")}</span>'
            f'</div>'
            f'<p style="margin: 8px 0; color:#9ca3af; font-size:0.9rem;">{todo.get("description", "")}</p>'
            f'<div style="display:flex; gap:20px; font-size:0.8rem; color:#6b7280; margin-bottom: 10px;">'
            f'<span>📅 Due: {due_date_val}</span>'
            f'<span>⏱ Status: {status_badge}</span>'
            f'<span>Created: {todo.get("created_at")[:10]}</span>'
            + (f'<span>Completed: {todo.get("completed_at")[:10]}</span>' if todo.get("completed_at") else '') +
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Action Buttons in columns directly underneath/beside
        btn_col1, btn_col2, btn_col3, _ = st.columns([1.5, 1, 1, 5])
        
        with btn_col1:
            if todo.get("status") == "Pending":
                if st.button("Done ✔", key=f"done_{tid}"):
                    update("todos", tid, {
                        "status": "Completed",
                        "completed_at": datetime.now().isoformat()
                    })
                    st.rerun()
            else:
                if st.button("Re-open ↩", key=f"reopen_{tid}"):
                    update("todos", tid, {
                        "status": "Pending",
                        "completed_at": None
                    })
                    st.rerun()
                    
        with btn_col2:
            if st.button("Edit 📝", key=f"edit_{tid}"):
                st.session_state.editing_todo_id = tid
                st.rerun()
                
        with btn_col3:
            if st.button("Delete 🗑", key=f"delete_{tid}"):
                # Soft delete: sets is_deleted = True and deleted_at
                update("todos", tid, {
                    "is_deleted": True,
                    "deleted_at": datetime.now().isoformat()
                })
                st.success("Task moved to History.")
                st.rerun()
                
        st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)
