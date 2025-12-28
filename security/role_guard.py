from functools import wraps
from flask import session, jsonify

def roles_required(*roles):
    """
    Decorator to ensure user has one of the required roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({"success": False, "message": "Authentication required"}), 401
            
            user_role = session['user'].get('role')
            if user_role not in roles and 'admin' not in roles: # Admin usually has access to everything, but let's be explicit
                 # If admin is not explicitly allowed, check if user is admin (super user)
                 if user_role == 'admin':
                     return f(*args, **kwargs)
                 return jsonify({"success": False, "message": "Insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_required(f):
    """
    Decorator to ensure user is logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"success": False, "message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function
