import time

# In-memory storage for failed attempts
# Format: {ip_address: {"attempts": count, "lockout_until": timestamp}}
failed_attempts = {}

MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 300 # 5 minutes

def record_failed_attempt(ip_address):
    """
    Records a failed login attempt for an IP.
    Returns True if user is now locked out.
    """
    current_time = time.time()
    
    if ip_address not in failed_attempts:
        failed_attempts[ip_address] = {"attempts": 0, "lockout_until": 0}
        
    data = failed_attempts[ip_address]
    
    # Reset attempts if lockout period has passed
    if data["lockout_until"] > 0 and current_time > data["lockout_until"]:
        data["attempts"] = 0
        data["lockout_until"] = 0
        
    data["attempts"] += 1
    
    if data["attempts"] >= MAX_ATTEMPTS:
        data["lockout_until"] = current_time + LOCKOUT_DURATION
        return True
        
    return False

def is_locked_out(ip_address):
    """
    Checks if an IP is currently locked out.
    """
    if ip_address not in failed_attempts:
        return False
        
    data = failed_attempts[ip_address]
    if data["lockout_until"] > time.time():
        return True
        
    return False

def reset_attempts(ip_address):
    """
    Resets failed attempts for an IP (e.g., after successful login).
    """
    if ip_address in failed_attempts:
        del failed_attempts[ip_address]
