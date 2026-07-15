import os
import json
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")

def get_file_path(table_name: str) -> str:
    """Returns the absolute file path for a given table name."""
    return os.path.join(DB_DIR, f"{table_name}.json")

def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Loads a JSON file and returns its content as a list of dictionaries."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_json(file_path: str, data: List[Dict[str, Any]]) -> bool:
    """Saves data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)
        return True
    except IOError:
        return False

def insert(table_name: str, record: Dict[str, Any]) -> bool:
    """Inserts a new record into the specified JSON database file."""
    file_path = get_file_path(table_name)
    data = load_json(file_path)
    data.append(record)
    return save_json(file_path, data)

def update(table_name: str, record_id: str, updated_fields: Dict[str, Any]) -> bool:
    """Updates specific fields of a record matching record_id in the JSON file."""
    file_path = get_file_path(table_name)
    data = load_json(file_path)
    updated = False
    for i, item in enumerate(data):
        if str(item.get("id")) == str(record_id) or (table_name == "users" and item.get("username", "").lower() == str(record_id).lower()):
            data[i].update(updated_fields)
            updated = True
            break
    if updated:
        return save_json(file_path, data)
    return False

def delete(table_name: str, record_id: str) -> bool:
    """Permanently deletes a record matching record_id from the JSON file."""
    file_path = get_file_path(table_name)
    data = load_json(file_path)
    original_len = len(data)
    data = [item for item in data if str(item.get("id")) != str(record_id)]
    if len(data) < original_len:
        return save_json(file_path, data)
    return False

def restore(table_name: str, record_id: str) -> bool:
    """Restores a soft-deleted todo by setting is_deleted=False and deleted_at=None."""
    return update(table_name, record_id, {"is_deleted": False, "deleted_at": None})

def find_by_id(table_name: str, record_id: str) -> Optional[Dict[str, Any]]:
    """Finds a single record by its id in the specified table."""
    file_path = get_file_path(table_name)
    data = load_json(file_path)
    for item in data:
        if str(item.get("id")) == str(record_id):
            return item
    return None

def find_by_username(table_name: str, username: str) -> List[Dict[str, Any]]:
    """Finds records belonging to a specific user.
    If table is 'users', returns a single user in a list (or empty).
    If table is 'todos', returns all todos matching the owner/username.
    """
    file_path = get_file_path(table_name)
    data = load_json(file_path)
    if table_name == "users":
        return [item for item in data if item.get("username", "").lower() == username.lower()]
    else:
        return [item for item in data if item.get("owner", "").lower() == username.lower()]
