from flask import Blueprint, request, jsonify, Response
from admin.settings_service import load_settings, save_settings, update_setting
from admin.account_service import get_all_accounts, create_account, update_account, delete_account
from admin.export_service import export_all_data

admin_bp = Blueprint('admin', __name__)

# --- Settings Endpoints ---
@admin_bp.route('/api/admin/settings', methods=['GET'])
def get_settings():
    return jsonify(load_settings())

@admin_bp.route('/api/public/settings', methods=['GET'])
def get_public_settings():
    settings = load_settings()
    # Filter only safe public fields
    public_data = {
        "theme": settings.get("theme", "dark"),
        "canteen_name": settings.get("canteen_name", "UMU SmartCaf"),
        "operating_year": settings.get("operating_year", 2025)
    }
    return jsonify(public_data)

@admin_bp.route('/api/admin/export', methods=['GET'])
def export_data_endpoint():
    export_format = request.args.get('format', 'json').lower()
    data, mime_type, filename = export_all_data(export_format)
    
    if data:
        return Response(
            data,
            mimetype=mime_type,
            headers={"Content-disposition": f"attachment; filename={filename}"}
        )
    return jsonify({"success": False, "message": "Failed to generate export"}), 500

@admin_bp.route('/api/admin/settings', methods=['POST'])
def save_all_settings():
    data = request.get_json()
    if save_settings(data):
        return jsonify({"success": True, "message": "Settings saved"})
    return jsonify({"success": False, "message": "Failed to save settings"}), 500

# --- Account Endpoints ---
@admin_bp.route('/api/admin/accounts', methods=['GET'])
def list_accounts():
    return jsonify({"success": True, "data": get_all_accounts()})

@admin_bp.route('/api/admin/accounts', methods=['POST'])
def add_account():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'staff')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400
        
    success, msg = create_account(username, email, password, role)
    if success:
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "message": msg}), 400

@admin_bp.route('/api/admin/accounts/<username>', methods=['PUT'])
def edit_account(username):
    data = request.get_json()
    success, msg = update_account(username, data)
    if success:
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "message": msg}), 400

@admin_bp.route('/api/admin/accounts/<username>', methods=['DELETE'])
def remove_account(username):
    success, msg = delete_account(username)
    if success:
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "message": msg}), 400
