from flask import Flask, send_from_directory, request, session, redirect, jsonify
from auth.auth_controller import auth_bp
from dashboard.dashboard_controller import dashboard_bp
from users.user_controller import users_bp
from attendance.attendance_controller import attendance_bp
from payments.payment_controller import payments_bp
from reports.report_controller import reports_bp
from training.training_controller import training_bp
from admin.settings_controller import admin_bp
from security.security_controller import security_bp
from support.support_controller import support_bp
from menu.menu_controller import menu_bp

import os

app = Flask(__name__, static_folder='.')

# Environment Configuration
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app.secret_key = os.getenv('SECRET_KEY', 'umu_smart_caf_secure_key_2025')

@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "message": "API endpoint not found"}), 404
    return send_from_directory('.', 'error-404.html'), 404

@app.before_request
def check_login():
    # List of public paths that don't require login
    public_paths = [
        '/',
        '/login.html', 
        '/api/login', 
        '/api/verify-2fa',
        '/register.html', 
        '/api/register', 
        '/forgot-password.html', 
        '/api/forgot-password', 
        '/logout-confirmation.html',
        '/api/public/settings'
    ]
    
    # Allow access to static assets (images, css, js) and public paths
    if (request.path in public_paths or 
        request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico')) or
        request.path.startswith('/static/')):
        return
        
    # Access Control Logic
    user = session.get('user')
    if not user:
        if request.path.startswith('/api/'):
            return jsonify({"success": False, "message": "Authentication required. Please log in."}), 401
        return redirect('/login.html')

    user_role = str(user.get('role', '')).lower()
    
    # 🕵️ Security Levels
    # 1. System Admin (Full Access: admin)
    # 2. Staff (Management Access: staff)
    # 3. Student (Restricted: student)
    
    # Strictly Admin Only
    admin_only_paths = [
        '/system-settings.html',
        '/account-management.html'
    ]
    
    # Admin or Staff
    management_paths = [
        '/finance-upload.html',
        '/bulk-payment.html',
        '/users-list.html',
        '/user-details.html',
        '/add-user.html',
        '/edit-user.html',
        '/attendance-control.html',
        '/reports-dashboard.html',
        '/attendance-report.html',
        '/payment-report.html',
        '/user-activity-report.html',
        '/menu-management.html'
    ]


    # Check Admin-Only
    if request.path in admin_only_paths or request.path.startswith('/api/admin/'):
        if user_role != 'admin':
            print(f"Access Denied to {request.path}: User {user.get('email')} is not an admin (Role: {user_role})")
            if request.path.startswith('/api/'):
                return jsonify({"success": False, "message": "Admin privileges required."}), 403
            return redirect('/dashboard.html')

    # Check Management (Admin or Staff)
    if request.path in management_paths:
        if user_role not in ['admin', 'staff']:
            print(f"Access Denied to {request.path}: User {user.get('email')} is not Staff/Admin (Role: {user_role})")
            return redirect('/dashboard.html')

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(users_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(training_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(security_bp)
app.register_blueprint(support_bp)
from payments.finance_controller import finance_bp
app.register_blueprint(finance_bp)
app.register_blueprint(menu_bp)


# Serve static files (HTML, CSS, JS, Images)
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

if __name__ == '__main__':
    print("Starting UMU SmartCaf Server...")
    print("Access the app at http://localhost:5000")
    app.run(debug=True, port=5000)
