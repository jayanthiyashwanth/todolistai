import bcrypt
from datetime import datetime
from typing import Dict, Any, Optional
from utils.database import get_file_path, load_json, insert, find_by_username

def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hashed bcrypt password."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def register_user(fullname: str, username: str, email: str, password: str) -> bool:
    """Registers a new user in users.json. Returns True if successful."""
    hashed = hash_password(password)
    user_record = {
        "fullname": fullname.strip(),
        "username": username.strip(),
        "email": email.strip().lower(),
        "password": hashed,
        "created_at": datetime.now().isoformat()
    }
    return insert("users", user_record)

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates user with username and password. Returns user object or None."""
    results = find_by_username("users", username)
    if not results:
        return None
    user = results[0]
    if verify_password(password, user.get("password", "")):
        return user
    return None
