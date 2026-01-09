import uuid
import random
import string

def generate_uuid():
    """
    Generates a standard UUID string.
    """
    return str(uuid.uuid4())

def generate_short_id(length=8):
    """
    Generates a short random ID consisting of uppercase letters and digits.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_ticket_id():
    """
    Generates a support ticket ID (e.g., TK-123456).
    """
    return f"TK-{generate_short_id(6)}"

def generate_transaction_id():
    """
    Generates a transaction ID (e.g., TXN-12345678).
    """
    return f"TXN-{generate_short_id(8)}"

def generate_umu_id(existing_users, role='Student'):
    """
    Generates a sequential role-based UMU ID in format:
    - Students: UMUSTUD20250001, UMUSTUD20250002, etc.
    - Staff: UMUSTAF20250001, UMUSTAF20250002, etc.
    - Admin: UMUADMIN20250001, UMUADMIN20250002, etc.
    
    Checks existing users to ensure no duplicates.
    """
    # Normalize role
    role = role.lower() if role else 'student'
    
    # Determine prefix based on role
    if role == 'staff':
        prefix = 'UMUSTAF'
    elif role == 'admin':
        prefix = 'UMUADMIN'
    else:  # Default to student
        prefix = 'UMUSTUD'
    
    # Extract all existing IDs with the same prefix
    existing_ids = []
    for user in existing_users:
        user_id = user.get('id', '')
        if user_id.startswith(prefix):
            try:
                # Extract the numeric part (e.g., 20250001 from UMUSTUD20250001)
                num_part = int(user_id[len(prefix):])
                existing_ids.append(num_part)
            except ValueError:
                continue
    
    # Find the next available number
    if existing_ids:
        next_num = max(existing_ids) + 1
    else:
        # Start from 20250001 if no existing IDs with this prefix
        next_num = 20250001
    
    return f"{prefix}{next_num}"
