from flask import Blueprint, request, jsonify
from training.training_service import authenticate_training, start_training_thread, get_training_status

training_bp = Blueprint('training', __name__)

@training_bp.route('/api/training/auth', methods=['POST'])
def auth():
    data = request.get_json()
    password = data.get('password')
    
    if authenticate_training(password):
        return jsonify({"success": True, "message": "Authenticated"})
    return jsonify({"success": False, "message": "Invalid password"}), 401

@training_bp.route('/api/training/start', methods=['POST'])
def start():
    success, msg = start_training_thread()
    if success:
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "message": msg}), 400

@training_bp.route('/api/training/status', methods=['GET'])
def status():
    return jsonify(get_training_status())
