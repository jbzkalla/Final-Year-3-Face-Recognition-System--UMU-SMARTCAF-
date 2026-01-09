import json
import hashlib

# Read users.json
with open('data/users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# Counters for each role
student_counter = 1
staff_counter = 1
admin_counter = 1

# Update each user's ID based on their role
for user in users:
    role = user.get('role', '').lower()
    
    if role == 'student':
        new_id = f"UMUSTUD{2025}{student_counter:04d}"
        student_counter += 1
    elif role == 'staff':
        new_id = f"UMUSTAF{2025}{staff_counter:04d}"
        staff_counter += 1
    elif role == 'admin':
        new_id = f"UMUADMIN{2025}{admin_counter:04d}"
        admin_counter += 1
    else:
        # Default to student if role is unclear
        new_id = f"UMUSTUD{2025}{student_counter:04d}"
        student_counter += 1
        user['role'] = 'Student'  # Normalize role
    
    # Update the user ID
    old_id = user.get('id', '')
    user['id'] = new_id
    
    # Update email to match new ID if it was auto-generated
    if 'email' in user and '@umu.ac.ug' in user['email']:
        # Check if email was auto-generated (contains old ID)
        if old_id.lower() in user['email'].lower() or user['email'].startswith('umu'):
            user['email'] = f"{new_id.lower()}@umu.ac.ug"
    
    print(f"Updated: {user.get('name', 'Unknown')} - {old_id} -> {new_id} ({user['role']})")

# Save updated users.json
with open('data/users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=4, ensure_ascii=False)

print(f"\n✓ Updated {len(users)} users")
print(f"  - Students: {student_counter - 1}")
print(f"  - Staff: {staff_counter - 1}")
print(f"  - Admins: {admin_counter - 1}")
