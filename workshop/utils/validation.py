import re
from typing import Dict, Any, Tuple
from utils.database import load_json, get_file_path

def validate_email(email: str) -> bool:
    """Validates if the email format is correct."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validates the password strength.
    Requires:
    - At least 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    - At least 1 special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    return True, "Password is strong."

def is_username_unique(username: str) -> bool:
    """Checks if the username is unique in the users database."""
    users = load_json(get_file_path("users"))
    for user in users:
        if user.get("username", "").lower() == username.lower():
            return False
    return True

def is_email_unique(email: str) -> bool:
    """Checks if the email is unique in the users database."""
    users = load_json(get_file_path("users"))
    for user in users:
        if user.get("email", "").lower() == email.lower():
            return False
    return True
