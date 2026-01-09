import json
import os
import re

def update_emails_unique():
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
    used_emails = set()
    print(f"Starting unique email update for {len(users)} users...")

    # Helper for name cleaning
    def get_name_parts(name):
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name).lower()
        return clean_name.split()

    # Define domains
    role_map = {
        'student': 'stud',
        'staff': 'staff',
        'admin': 'admin'
    }

    # Iterate through users
    for user in users:
        name = user.get('name', '').strip()
        role = user.get('role', 'student').lower()
        domain = role_map.get(role, 'stud')
        
        parts = get_name_parts(name)
        if not parts:
            continue

        first = parts[0]
        last = parts[-1] if len(parts) > 1 else ""

        # Try format 1: first.last
        if last:
            suggestion = f"{first}.{last}@{domain}.umu.ac.ug"
        else:
            suggestion = f"{first}@{domain}.umu.ac.ug"

        # Check collision
        if suggestion in used_emails:
            # Format 2: Shuffle (last.first)
            if last:
                suggestion = f"{last}.{first}@{domain}.umu.ac.ug"
            
            # If still collision (could happen if name is same but role diff?), add a number or try mid name
            if suggestion in used_emails and len(parts) > 2:
                # Format 3: first.middle.last
                mid = parts[1]
                suggestion = f"{first}.{mid}.{last}@{domain}.umu.ac.ug"

            # Final safety: append counter
            counter = 1
            original_suggestion = suggestion.split('@')[0]
            while suggestion in used_emails:
                suggestion = f"{original_suggestion}{counter}@{domain}.umu.ac.ug"
                counter += 1

        user['email'] = suggestion
        used_emails.add(suggestion)
        updated_count += 1
        print(f"Assigned: {name} -> {suggestion}")

    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
        print(f"\nSuccessfully synchronized {updated_count} unique user emails!")
    except Exception as e:
        print(f"Error saving database: {e}")

if __name__ == "__main__":
    update_emails_unique()
