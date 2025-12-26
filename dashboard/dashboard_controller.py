from flask import Blueprint, jsonify
from dashboard.dashboard_service import get_dashboard_stats

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    from flask import session
    user = session.get('user')
    if not user:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    role = user.get('role', 'student').lower()
    
    if role in ['admin', 'staff']:
        stats = get_dashboard_stats()
    else:
        # Student specific stats
        from dashboard.dashboard_service import get_student_stats
        stats = get_student_stats(user['id'])
        
    return jsonify({"success": True, "data": stats})

@dashboard_bp.route('/api/dashboard/notifications', methods=['GET'])
def notifications():
    from dashboard.dashboard_service import get_recent_notifications
    notifs = get_recent_notifications()
    return jsonify({"success": True, "data": notifs})
