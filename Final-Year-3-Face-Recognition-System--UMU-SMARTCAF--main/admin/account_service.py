from utils.constants import USERS_DB_FILE
from data.file_manager import read_json, write_json
from auth.password_utils import hash_password
from utils.id_generator import generate_short_id
import datetime

def get_all_accounts():
    """
    Returns a list of all accounts (excluding sensitive data like password hashes).
    """
    users = read_json(USERS_DB_FILE, default=[])
    accounts = []
    for user in users:
        accounts.append({
            "id": user.get("id"),
            "username": user.get("username", user.get("name")), # Fallback to name if username missing
            "email": user.get("email", ""),
            "role": user.get("role", "user"),
            "status": "Active" # Mock status
        })
    return accounts

def create_account(username, email, password, role="staff"):
    users = read_json(USERS_DB_FILE, default=[])
    
    if any(u.get('username') == username for u in users):
        return False, "Username already exists"
    
    new_user = {
        "id": generate_short_id(),
        "username": username,
        "name": username,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    users.append(new_user)
    if write_json(USERS_DB_FILE, users):
        return True, "Account created successfully"
    return False, "Failed to save account"

def update_account(username, data):
    users = read_json(USERS_DB_FILE, default=[])
    updated = False
    
    for i, user in enumerate(users):
        if user.get('username') == username:
            if "email" in data:
                users[i]["email"] = data["email"]
            if "role" in data:
                users[i]["role"] = data["role"]
            if "password" in data and data["password"]:
                users[i]["password_hash"] = hash_password(data["password"])
            updated = True
            break
            
    if updated:
        if write_json(USERS_DB_FILE, users):
            return True, "Account updated"
    return False, "User not found"

def delete_account(username):
    users = read_json(USERS_DB_FILE, default=[])
    
    if username == "admin": # Prevent deleting main admin
        return False, "Cannot delete main admin account"
        
    initial_len = len(users)
    users = [u for u in users if u.get('username') != username]
    
    if len(users) < initial_len:
        if write_json(USERS_DB_FILE, users):
            return True, "Account deleted"
            
    return False, "User not found"
