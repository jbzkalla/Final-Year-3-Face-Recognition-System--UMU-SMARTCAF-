from flask import Blueprint, request, jsonify, session
from auth.auth_service import authenticate_user, reset_password, register_user
from utils.constants import STATUS_SUCCESS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email') or data.get('username')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    result = authenticate_user(email, password)
    if result.get("status") == STATUS_SUCCESS:
        user = result.get("user")
        
        # Check if 2FA is globally enabled
        from admin.settings_service import load_settings
        settings = load_settings()
        
        # 2FA applies to Management roles if enabled
        if settings.get('enable_2fa') and user['role'].lower() in ['admin', 'staff']:
            # Instead of logging in, return that 2FA is required
            # Store temporary user info in session for verification
            session['temp_user'] = user
            return jsonify({
                "success": True, 
                "requires_2fa": True, 
                "message": "Double-factor verification required."
            })

        session['user'] = user
        return jsonify({"success": True, "message": "Login successful", "role": user["role"]})
    else:
        return jsonify({"success": False, "message": result.get("message", "Invalid credentials")}), 401

@auth_bp.route('/api/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json()
    code = data.get('code')
    
    # Debug logging to terminal
    print(f"DEBUG: 2FA Verification Attempt - Code Received: '{code}' (Type: {type(code)})")
    
    if not session.get('temp_user'):
        print("DEBUG: 2FA Failed - No temporary user in session.")
        return jsonify({"success": False, "message": "Session expired. Please login again."}), 401
    
    # Simulation: Verification code is always 233273
    # Robust comparison: convert to string and strip any accidental whitespace
    if str(code).strip() == "233273":
        user = session.pop('temp_user')
        session['user'] = user
        print(f"DEBUG: 2FA Success - User: {user.get('email')}")
        return jsonify({"success": True, "message": "Verification successful", "role": user["role"]})
    else:
        print(f"DEBUG: 2FA Failed - Invalid code '{code}' entered.")
        return jsonify({"success": False, "message": "Invalid verification code"}), 400

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True, "message": "Logged out successfully"})

@auth_bp.route('/api/session', methods=['GET'])
def get_session_user():
    user = session.get('user')
    if user:
        # Re-fetch from DB or enrichment if needed, for legacy we return session
        return jsonify({"success": True, "user": user})
    return jsonify({"success": False, "message": "No active session"}), 401

@auth_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400

    if reset_password(email):
        return jsonify({"success": True, "message": "Password reset link sent to your email"})
    else:
        # For security, we might want to return success even if email not found, 
        # but for this internal app, explicit error is fine.
        return jsonify({"success": False, "message": "Email not found"}), 404


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if register_user(username, email, password):
        return jsonify({"success": True, "message": "Registration successful"})
    else:
        return jsonify({"success": False, "message": "Username already exists"}), 409
