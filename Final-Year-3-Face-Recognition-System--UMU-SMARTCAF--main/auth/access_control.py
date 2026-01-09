from functools import wraps
from flask import session, jsonify, redirect, url_for, request

def login_required(f):
    """
    Decorator to restrict access to authenticated users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            # If it's an API request, return JSON error
            if request.path.startswith('/api/'):
                return jsonify({"success": False, "message": "Authentication required"}), 401
            # If it's a page request, redirect to login
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to restrict access to Admin users only.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"success": False, "message": "Authentication required"}), 401
            return redirect(url_for('auth.login_page'))
        
        user = session.get('user')
        if user.get('role') != 'Admin':
            if request.path.startswith('/api/'):
                return jsonify({"success": False, "message": "Admin privileges required"}), 403
            return redirect(url_for('dashboard.index')) # Or access denied page
            
        return f(*args, **kwargs)
    return decorated_function
