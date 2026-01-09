from utils.constants import USERS_DB_FILE
from data.file_manager import read_json, write_json
from utils.id_generator import generate_short_id
from auth.password_utils import hash_password
import datetime

def get_all_users():
    data = read_json(USERS_DB_FILE, default=[])
    if not isinstance(data, list):
        return []
    return data

def get_user_by_id(user_id):
    users = get_all_users()
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def create_user(data):
    users = get_all_users()
    
    # Get role and name
    role = data.get('role', 'Student')
    name = data.get('name', '').strip()
    
    # Generate Unique Email based on formatting rules
    def get_clean_parts(n):
        import re
        clean = re.sub(r'[^a-zA-Z\s]', '', n).lower()
        return clean.split()

    name_parts = get_clean_parts(name)
    first = name_parts[0] if name_parts else "user"
    last = name_parts[-1] if len(name_parts) > 1 else ""
    
    role_map = {'student': 'stud', 'staff': 'staff', 'admin': 'admin'}
    domain = role_map.get(role.lower(), 'stud')
    
    # Suggestion 1: first.last
    email_suggestion = f"{first}.{last}@{domain}.umu.ac.ug" if last else f"{first}@{domain}.umu.ac.ug"
    
    # Check for collision in current DB
    if any(u.get('email') == email_suggestion for u in users):
        # Shuffle: last.first
        if last:
            email_suggestion = f"{last}.{first}@{domain}.umu.ac.ug"
        
        # If STILL collision, add a number (safety fallback)
        counter = 1
        base_prefix = email_suggestion.split('@')[0]
        while any(u.get('email') == email_suggestion for u in users):
            email_suggestion = f"{base_prefix}{counter}@{domain}.umu.ac.ug"
            counter += 1
            
    # Use the generated unique email (or the one provided if manually edited - 
    # but based on your request, we prioritize this auto-generation logic)
    final_email = data.get('email', email_suggestion)
    # Re-verify manual email uniqueness
    if any(u.get('email') == final_email for u in users) and final_email != email_suggestion:
         final_email = email_suggestion # fallback to safe unique one
    
    # Import here to avoid circular dependency
    from utils.id_generator import generate_umu_id
    
    # Determine default password based on role
    role_lower = role.lower()
    default_pass = "stud123"
    if role_lower == "admin": default_pass = "admin123"
    elif role_lower == "staff": default_pass = "staff123"
    
    new_user = {
        "id": generate_umu_id(users, role),  # Generate sequential role-based UMU ID
        "name": name,
        "email": final_email,
        "role": role,
        "department": data.get('department', ''),
        "password_hash": hash_password(data.get('password', default_pass)), # Use role-specific default
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    users.append(new_user)
    if write_json(USERS_DB_FILE, users):
        return True, new_user
    return False, "Failed to save user"

def update_user(user_id, data):
    users = get_all_users()
    updated = False
    for i, user in enumerate(users):
        if user['id'] == user_id:
            users[i].update(data)
            updated = True
            break
    
    if updated:
        if write_json(USERS_DB_FILE, users):
            return users[i]
    return None

def delete_user(user_id):
    users = get_all_users()
    initial_len = len(users)
    users = [u for u in users if u['id'] != user_id]
    
    if len(users) < initial_len:
        if write_json(USERS_DB_FILE, users):
            return True, "User deleted"
    return False, "User not found"
def delete_users_bulk(user_ids):
    users = get_all_users()
    initial_len = len(users)
    users = [u for u in users if u['id'] not in user_ids]
    
    if len(users) < initial_len:
        if write_json(USERS_DB_FILE, users):
            return True, f"Deleted {initial_len - len(users)} users"
    return False, "No users found or failed to update"
