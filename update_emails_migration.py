import json
import os
import re

def update_emails():
    db_path = r'c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project\data\users.json'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except Exception as e:
        print(f"Error reading database: {e}")
        return

    updated_count = 0
    print(f"Starting email update for {len(users)} users...")

    for user in users:
        name = user.get('name', '').strip()
        role = user.get('role', 'student').lower()
        old_email = user.get('email', 'N/A')

        if not name:
            continue

        # Convert "First Last" to "first.last"
        # Remove special characters and replace multiple spaces with single dot
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name).lower()
        name_parts = clean_name.split()
        
        if len(name_parts) >= 2:
            email_prefix = f"{name_parts[0]}.{name_parts[-1]}"
        else:
            email_prefix = name_parts[0] if name_parts else "user"

        # Map roles to email domains
        role_map = {
            'student': 'stud',
            'staff': 'staff',
            'admin': 'admin'
        }
        domain = role_map.get(role, 'stud')
        
        new_email = f"{email_prefix}@{domain}.umu.ac.ug"
        
        if old_email != new_email:
            user['email'] = new_email
            print(f"Updated: {name} | {old_email} -> {new_email}")
            updated_count += 1

    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
        print(f"\nSuccessfully updated {updated_count} user emails!")
    except Exception as e:
        print(f"Error saving database: {e}")

if __name__ == "__main__":
    update_emails()
