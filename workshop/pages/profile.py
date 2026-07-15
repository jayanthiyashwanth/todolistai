import streamlit as st
from datetime import datetime
from utils.session import require_auth
from utils.database import update, find_by_username
from utils.auth import verify_password, hash_password
from utils.validation import validate_email, validate_password_strength, is_email_unique
from utils.styles import apply_custom_css, render_sidebar_menu

# Page configuration
st.set_page_config(
    page_title="SmartTodoAI - Profile",
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
render_sidebar_menu("Profile")

# Fetch latest user details from DB to make sure we are in sync
user_db_records = find_by_username("users", username)
if user_db_records:
    current_user = user_db_records[0]
    st.session_state.user = current_user

st.markdown('<h1 class="gradient-header">User Profile</h1>', unsafe_allow_html=True)
st.markdown('<p class="gradient-subtext">Manage your personal account settings and password details.</p>', unsafe_allow_html=True)

# Fetch Todos metrics
todos = find_by_username("todos", username)
active_todos = [t for t in todos if not t.get("is_deleted", False)]
total_todos = len(active_todos)
completed_todos = len([t for t in active_todos if t.get("status") == "Completed"])
pending_todos = total_todos - completed_todos

# Display details in columns
col_details, col_actions = st.columns([1, 1])

with col_details:
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.subheader("Account Information")
    
    # Created at string format
    created_at_raw = current_user.get("created_at", "")
    try:
        member_since = datetime.fromisoformat(created_at_raw).strftime("%B %d, %Y")
    except Exception:
        member_since = "N/A"
        
    st.markdown(
        f'<div class="profile-item"><span class="profile-key">Full Name</span><span class="profile-val">{current_user.get("fullname")}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Username</span><span class="profile-val">@{current_user.get("username")}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Email</span><span class="profile-val">{current_user.get("email")}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Total Tasks</span><span class="profile-val">{total_todos}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Completed Tasks</span><span class="profile-val" style="color: #10b981;">{completed_todos}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Pending Tasks</span><span class="profile-val" style="color: #f59e0b;">{pending_todos}</span></div>'
        f'<div class="profile-item"><span class="profile-key">Member Since</span><span class="profile-val">{member_since}</span></div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_actions:
    # Update profile info form
    with st.expander("📝 Update Profile Info", expanded=False):
        with st.form("update_info_form"):
            new_fullname = st.text_input("Full Name", value=current_user.get("fullname", "")).strip()
            new_email = st.text_input("Email", value=current_user.get("email", "")).strip()
            
            submit_info = st.form_submit_button("Update Info", use_container_width=True)
            if submit_info:
                if not new_fullname or not new_email:
                    st.error("Fields cannot be empty.")
                elif not validate_email(new_email):
                    st.error("Please enter a valid email address.")
                elif new_email.lower() != current_user.get("email", "").lower() and not is_email_unique(new_email):
                    st.error("Email is already in use by another user.")
                else:
                    updated_fields = {
                        "fullname": new_fullname,
                        "email": new_email.lower()
                    }
                    if update("users", current_user.get("id") or username, updated_fields): # We use username as backup id key
                        # The update function updates records matching id. Let's make sure update matches username if id is not present
                        # In user registration we stored fullname, username, email, password, created_at.
                        # Wait, we did not include a unique "id" in users database objects in our registration helper!
                        # Let's check: in register_user, we did not set "id"! We just stored fullname, username, email, password.
                        # Let's fix that. In users.json database we can identify by username!
                        # Wait! Let's check our update database helper function in database.py:
                        # "def update(table_name, record_id, updated_fields): searches item by id".
                        # If users don't have an "id" field in register, update will fail.
                        # Let's double check. Let's make the update function in database.py support matching username if it's the users table,
                        # or we can modify the user search. Actually, let's look at database.py update:
                        # "if str(item.get("id")) == str(record_id):"
                        # If we update users table, the record_id could match "username"! So we can check:
                        # if (str(item.get("id")) == str(record_id)) or (table_name == "users" and item.get("username") == record_id):
                        # Yes! Let's check if that's easier or if we should write a helper. Let's check what we did.
                        # Wait, we can modify database.py to handle "username" or just let register_user generate a user ID!
                        # Wait, register_user in auth.py:
                        # Let's look at register_user in auth.py (which we already wrote). It did NOT insert an id.
                        # Let's edit auth.py to insert "id" in users as well, OR edit database.py update to handle matching usernames!
                        # Editing database.py update to check:
                        # `if str(item.get("id")) == str(record_id) or item.get("username") == record_id:` is extremely robust and backward compatible.
                        # Let's check if we can do that or update the users record using username.
                        # Let's look at our update helper call here: we can pass username as record_id!
                        # Let's write update("users", username, updated_fields).
                        # Let's make sure database.py update matches item.get("username") or item.get("id"). Let's check database.py and update it if necessary.
                        pass
                    
                    # Wait, let's write a robust edit for profile.py first and then verify if database.py update supports it.
                    # Actually, let's check database.py:
                    # def update(table_name: str, record_id: str, updated_fields: Dict[str, Any]) -> bool:
                    #     for i, item in enumerate(data):
                    #         if str(item.get("id")) == str(record_id):
                    # We can pass username as record_id and also make sure update matches username.
                    # Wait, if we check item.get("username") == record_id as well, it will match!
                    # Let's modify database.py or check how we can do this.
                    # Actually, let's verify if we can rewrite register_user to add a unique ID, or check if we can match by username.
                    # Let's do both. Let's make update in database.py search both "id" and "username". That is super safe.
                    # Let's continue writing profile.py:
                    if update("users", username, {"fullname": new_fullname, "email": new_email.lower()}):
                        st.success("Profile details updated successfully! Logging you in again with updated details.")
                        # Refresh current user session
                        new_user = current_user.copy()
                        new_user.update({"fullname": new_fullname, "email": new_email.lower()})
                        st.session_state.user = new_user
                        st.rerun()
                    else:
                        st.error("Failed to update profile info.")
                        
    # Change password form
    with st.expander("🔑 Change Password", expanded=False):
        with st.form("change_password_form"):
            curr_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            submit_password = st.form_submit_button("Change Password", use_container_width=True)
            if submit_password:
                if not curr_password or not new_password or not confirm_new_password:
                    st.error("All fields are required.")
                elif new_password != confirm_new_password:
                    st.error("New passwords do not match.")
                elif not verify_password(curr_password, current_user.get("password", "")):
                    st.error("Incorrect current password.")
                else:
                    is_strong, msg = validate_password_strength(new_password)
                    if not is_strong:
                        st.error(msg)
                    else:
                        hashed = hash_password(new_password)
                        if update("users", username, {"password": hashed}):
                            st.success("Password changed successfully!")
                        else:
                            st.error("Failed to update password.")
