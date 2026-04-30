from flask import Blueprint, request, jsonify
import os
import datetime
from users.user_service import get_all_users, get_user_by_id, create_user, update_user, delete_user, delete_users_bulk
from users.user_validator import validate_user_data
from users.face_capture_service import save_face_image, has_face_data
from utils.constants import IMAGES_DIR

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET'])
def list_users():
    users = get_all_users()
    # Enrich with face data status
    for user in users:
        user['has_face_data'] = has_face_data(user['id'])
    return jsonify({"success": True, "data": users})

@users_bp.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify({"success": False, "message": error}), 400
    
    success, new_user = create_user(data)
    if success:
        return jsonify({"success": True, "message": "User created successfully", "data": new_user}), 201
    else:
        return jsonify({"success": False, "message": new_user}), 500

@users_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        user['has_face_data'] = has_face_data(user_id)
        
        # Add last capture timestamp
        user['last_capture_time'] = "N/A"
        user_folder = os.path.join(IMAGES_DIR, str(user_id))
        if os.path.exists(user_folder):
             files = [f for f in os.listdir(user_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
             if files:
                 files.sort(key=lambda x: os.path.getmtime(os.path.join(user_folder, x)), reverse=True)
                 mtime = os.path.getmtime(os.path.join(user_folder, files[0]))
                 user['last_capture_time'] = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                 
        return jsonify({"success": True, "data": user})
    return jsonify({"success": False, "message": "User not found"}), 404

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    data = request.get_json()
    updated_user = update_user(user_id, data)
    if updated_user:
        return jsonify({"success": True, "message": "User updated successfully", "data": updated_user})
    return jsonify({"success": False, "message": "User not found"}), 404

@users_bp.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    if delete_user(user_id):
        return jsonify({"success": True, "message": "User deleted successfully"})
    return jsonify({"success": False, "message": "User not found"}), 404

@users_bp.route('/api/admin/users/bulk-delete', methods=['POST'])
def bulk_delete_users():
    data = request.get_json()
    user_ids = data.get('ids', [])
    if not user_ids:
        return jsonify({"success": False, "message": "No user IDs provided"}), 400
    
    success, message = delete_users_bulk(user_ids)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400

@users_bp.route('/api/users/capture', methods=['POST'])
def capture_face():
    data = request.get_json()
    user_id = data.get('user_id')
    image_data = data.get('image')
    
    if not user_id or not image_data:
        return jsonify({"success": False, "message": "User ID and image data required"}), 400
        
    success, result = save_face_image(user_id, image_data)
    if success:
        return jsonify({"success": True, "message": "Face image captured successfully", "path": result})
    else:
        return jsonify({"success": False, "message": f"Failed to save image: {result}"}), 500

@users_bp.route('/api/users/<user_id>/image')
def get_user_profile_image(user_id):
    from flask import send_from_directory
    
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    if not os.path.exists(user_folder):
        return jsonify({"success": False, "message": "No images found"}), 404
        
    try:
        files = [f for f in os.listdir(user_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if not files:
            return jsonify({"success": False, "message": "No images found"}), 404
            
        # Get the latest image
        files.sort(key=lambda x: os.path.getmtime(os.path.join(user_folder, x)), reverse=True)
        return send_from_directory(user_folder, files[0])
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
