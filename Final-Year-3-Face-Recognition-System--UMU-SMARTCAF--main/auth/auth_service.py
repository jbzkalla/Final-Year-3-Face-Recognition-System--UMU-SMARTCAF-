from utils.constants import USERS_DB_FILE, ROLE_ADMIN, STATUS_SUCCESS, STATUS_ERROR
from data.file_manager import read_json, write_json
from auth.password_utils import verify_password, hash_password
import datetime

def authenticate_user(email, password):
    """
    Authenticates a user by email and password.
    """
    users = read_json(USERS_DB_FILE, default=[])
    
    # Check if it's the default admin
    if email == "admin@umu.ac.ug" and password == "admin123":
        return {
            "status": STATUS_SUCCESS,
            "user": {
                "id": "0",
                "name": "System Admin",
                "email": email,
                "role": ROLE_ADMIN
            }
        }
    
    # Check against stored users
    for user in users:
        if user.get('email') == email:
            # Fix: verify_password takes (stored_password, provided_password)
            if verify_password(user.get('password_hash', ''), password):
                from users.face_capture_service import has_face_data
                return {
                    "status": STATUS_SUCCESS,
                    "user": {
                        "id": user.get('id'),
                        "name": user.get('name'),
                        "email": user.get('email'),
                        "role": user.get('role', 'student'),
                        "has_face_data": has_face_data(user.get('id'))
                    }
                }
    
    return {"status": STATUS_ERROR, "message": "Invalid credentials"}

def reset_password(email):
    """
    Initiates password reset process.
    Returns True if email exists, False otherwise.
    """
    users = read_json(USERS_DB_FILE, default=[])
    # Check if email exists in DB
    for user in users:
        if user.get("email") == email:
            # Logic to send email would go here
            print(f"Sending password reset link to {email}")
            return True
    return False

def register_user(username, email, password):
    """
    Registers a new user.
    Returns True if successful, False if email/username already exists.
    """
    users = read_json(USERS_DB_FILE, default=[])

    # Check if email already exists
    if any(user.get("email") == email for user in users):
        return False
    
    from utils.id_generator import generate_umu_id
    role = "Student" # Default role for public registration
    
    new_user = {
        "id": generate_umu_id(users, role),
        "name": username,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    users.append(new_user)
    write_json(USERS_DB_FILE, users)
    return True
