import json

# Read users.json
with open('data/users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# Verify IDs
print("=" * 60)
print("USER ID VERIFICATION REPORT")
print("=" * 60)

students = []
staff = []
admins = []

for user in users:
    user_id = user.get('id', '')
    role = user.get('role', '').lower()
    name = user.get('name', 'Unknown')
    
    if user_id.startswith('UMUSTUD'):
        students.append((user_id, name))
    elif user_id.startswith('UMUSTAF'):
        staff.append((user_id, name))
    elif user_id.startswith('UMUADMIN'):
        admins.append((user_id, name))
    else:
        print(f"⚠️  WARNING: Invalid ID format: {user_id} for {name}")

print(f"\n📊 SUMMARY:")
print(f"   Total Users: {len(users)}")
print(f"   Students: {len(students)}")
print(f"   Staff: {len(staff)}")
print(f"   Admins: {len(admins)}")

# Check for sequential order
def check_sequential(user_list, role_name):
    print(f"\n✅ {role_name} IDs (First 5 and Last 5):")
    issues = []
    
    # Show first 5
    for i, (uid, name) in enumerate(user_list[:5], 1):
        print(f"   {i}. {uid} - {name}")
    
    if len(user_list) > 10:
        print(f"   ... ({len(user_list) - 10} more)")
    
    # Show last 5
    if len(user_list) > 5:
        for i, (uid, name) in enumerate(user_list[-5:], len(user_list) - 4):
            print(f"   {i}. {uid} - {name}")
    
    # Verify sequential numbering
    for i, (uid, name) in enumerate(user_list, 1):
        expected_num = f"{2025}{i:04d}"
        if not uid.endswith(expected_num):
            issues.append(f"   ⚠️  {uid} should end with {expected_num}")
    
    if issues:
        print(f"\n⚠️  Issues found in {role_name}:")
        for issue in issues:
            print(issue)
    else:
        print(f"   ✓ All {role_name} IDs are sequential and correct!")

check_sequential(students, "STUDENTS")
check_sequential(staff, "STAFF")
check_sequential(admins, "ADMINS")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
