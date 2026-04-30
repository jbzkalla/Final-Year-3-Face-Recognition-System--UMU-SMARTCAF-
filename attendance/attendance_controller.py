from flask import Blueprint, request, jsonify
from attendance.session_manager import start_session, stop_session, get_active_session
from attendance.recognition_service import recognize_face
from attendance.attendance_service import mark_attendance, get_session_stats, get_recent_logs
from users.user_service import get_user_by_id

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/api/attendance/session', methods=['GET'])
def get_session():
    return jsonify(get_active_session())

@attendance_bp.route('/api/attendance/session', methods=['POST'])
def start_session_endpoint():
    data = request.get_json()
    session_name = data.get('name')
    mode = data.get('mode', 'continuous')
    
    if not session_name:
        return jsonify({"success": False, "message": "Session name required"}), 400
        
    success, message = start_session(session_name, mode)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400

@attendance_bp.route('/api/attendance/session', methods=['DELETE'])
def stop_session_endpoint():
    success, message = stop_session()
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400

@attendance_bp.route('/api/attendance/recognize', methods=['POST'])
def recognize_endpoint():
    data = request.get_json()
    image_data = data.get('image')
    save = data.get('save', True) # Default to true for backward compatibility
    
    if not image_data:
        return jsonify({"success": False, "message": "Image required"}), 400

    # 1. Recognize Face
    rec_result = recognize_face(image_data)
    user_id = rec_result.get('user_id')
    confidence = rec_result.get('confidence', 0)
    facial_area = rec_result.get('facial_area')
    is_live = rec_result.get('is_live', True)
    
    if user_id:
        if save:
            # 2. Mark Attendance immediately
            result = mark_attendance(user_id, confidence)
            user = get_user_by_id(user_id)
            
            # Add vision and identity feedback data
            result['recognised'] = True
            result['facial_area'] = facial_area
            result['is_live'] = is_live
            result['role'] = user['role'] if user else "Unknown"
            
            # 3. Handle Single User Mode Termination
            session = get_active_session()
            if session.get('mode') == 'single':
                stop_session()
                result['session_terminated'] = True
                
            return jsonify(result)
        else:
            # Only return recognition result
            user = get_user_by_id(user_id)
            return jsonify({
                "success": True,
                "recognised": True,
                "user_id": user_id,
                "name": user['name'] if user else "Unknown User",
                "role": user['role'] if user else "Unknown",
                "confidence": confidence,
                "facial_area": facial_area,
                "is_live": is_live
            })
    else:
        return jsonify({
            "success": False, 
            "message": "Face not recognized", 
            "confidence": confidence,
            "facial_area": facial_area,
            "is_live": is_live
        }), 401

@attendance_bp.route('/api/attendance/save', methods=['POST'])
def save_attendance_endpoint():
    data = request.get_json()
    user_id = data.get('user_id')
    confidence = data.get('confidence', 0)
    terminate = data.get('terminate', False)
    
    if not user_id:
        return jsonify({"success": False, "message": "User ID required"}), 400
        
    result = mark_attendance(user_id, confidence)
    if terminate:
        stop_session()
        result['session_terminated'] = True
        
    return jsonify(result)

@attendance_bp.route('/api/attendance/live', methods=['GET'])
def live_stats():
    stats = get_session_stats()
    logs = get_recent_logs()
    session = get_active_session()
    
    return jsonify({
        "session": session,
        "stats": stats,
        "logs": logs
    })
