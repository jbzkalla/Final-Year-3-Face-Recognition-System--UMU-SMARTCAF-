import hashlib
import os

def hash_password(password):
    """
    Hashes a password using SHA256 with a salt.
    Returns a hex-encoded string for JSON serialization.
    """
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    # Return as hex string for JSON serialization
    return (salt + key).hex()

def verify_password(stored_password, provided_password):
    """
    Verifies a stored password against a provided password.
    Handles both hex-encoded strings (new format) and bytes (legacy format).
    """
    # Convert hex string to bytes if needed
    if isinstance(stored_password, str):
        try:
            stored_password = bytes.fromhex(stored_password)
        except ValueError:
            return False
    
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    return new_key == stored_key
