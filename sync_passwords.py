from auth.password_utils import hash_password
from data.file_manager import read_json, write_json
import os

USERS_DB_FILE = "data/users.json"

def sync_passwords():
    if not os.path.exists(USERS_DB_FILE):
        print("Users file not found.")
        return

    users = read_json(USERS_DB_FILE)
    if not users:
        print("No users found.")
        return

    count = 0
    for user in users:
        role = user.get('role', 'Student').lower()
        if role == 'admin':
            new_pass = 'admin123'
        elif role == 'staff':
            new_pass = 'staff123'
        else:
            new_pass = 'stud123'
        
        user['password_hash'] = hash_password(new_pass)
        count += 1
    
    write_json(USERS_DB_FILE, users)
    print(f"Successfully synchronized {count} user passwords.")

if __name__ == "__main__":
    sync_passwords()
