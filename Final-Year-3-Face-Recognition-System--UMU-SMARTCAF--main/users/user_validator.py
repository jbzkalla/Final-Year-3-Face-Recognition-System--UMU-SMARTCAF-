import re

def validate_user_data(data):
    """
    Validates user data for creation or update.
    Returns (True, None) if valid, (False, error_message) if invalid.
    """
    if not data:
        return False, "No data provided"

    required_fields = ['name', 'email', 'role']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"

    # Email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['email']):
        return False, "Invalid email format"

    return True, None
