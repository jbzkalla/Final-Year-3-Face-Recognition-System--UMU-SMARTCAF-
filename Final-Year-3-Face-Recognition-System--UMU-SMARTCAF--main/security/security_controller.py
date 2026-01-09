from flask import Blueprint, jsonify, send_file
from security.audit_logger import get_logs, export_logs_to_csv
from security.role_guard import roles_required
import os

security_bp = Blueprint('security', __name__)

@security_bp.route('/api/security/logs', methods=['GET'])
@roles_required('admin')
def get_audit_logs():
    """
    Returns system audit logs. Only accessible by admins.
    """
    logs = get_logs()
    return jsonify({"success": True, "data": logs})

@security_bp.route('/api/security/logs/export', methods=['GET'])
@roles_required('admin')
def export_audit_logs():
    """
    Exports system audit logs to a CSV file. Only accessible by admins.
    """
    filepath = export_logs_to_csv()
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
    return jsonify({"success": False, "message": "Failed to export logs"}), 500
