from flask import Blueprint, request, jsonify, session
from menu.menu_service import (
    get_all_menu_items, get_menu_by_date, add_menu_item, 
    update_menu_item, delete_menu_item, toggle_availability,
    vote_on_item, bulk_toggle_availability, delete_menu_items_bulk
)
from datetime import datetime

menu_bp = Blueprint('menu', __name__)

# Student Endpoints
@menu_bp.route('/api/menu/today', methods=['GET'])
def get_today_menu():
    today = datetime.now().strftime('%Y-%m-%d')
    items = get_menu_by_date(today)
    return jsonify({"success": True, "data": items})

@menu_bp.route('/api/menu/all', methods=['GET'])
def get_all_items():
    items = get_all_menu_items()
    return jsonify({"success": True, "data": items})

@menu_bp.route('/api/menu/<item_id>/vote', methods=['POST'])
def vote(item_id):
    vote_type = request.json.get('vote') # 'like' or 'dislike'
    prev_vote = request.json.get('prev_vote') # 'like' or 'dislike' or None
    success, message = vote_on_item(item_id, vote_type, prev_vote)
    return jsonify({"success": success, "message": message})

# Admin Endpoints
@menu_bp.route('/api/admin/menu', methods=['POST'])
def create_item():
    data = request.form.to_dict()
    image = request.files.get('image')
    data['is_available'] = data.get('is_available', 'true').lower() == 'true'
    success, message, item = add_menu_item(data, image)
    return jsonify({"success": success, "message": message, "data": item})

@menu_bp.route('/api/admin/menu/<item_id>', methods=['POST'])
def edit_item(item_id):
    data = request.form.to_dict()
    image = request.files.get('image')
    if 'is_available' in data:
        data['is_available'] = data.get('is_available').lower() == 'true'
    success, message = update_menu_item(item_id, data, image)
    return jsonify({"success": success, "message": message})

@menu_bp.route('/api/admin/menu/bulk-toggle', methods=['POST'])
def bulk_toggle():
    data = request.json
    date_str = data.get('date') # Can be None for global toggle
    time_served = data.get('time_served', 'All') # 'Breakfast', 'Lunch', 'Supper', 'All'
    status = data.get('status', False)
    success, message = bulk_toggle_availability(date_str, time_served, status)
    return jsonify({"success": success, "message": message})

@menu_bp.route('/api/admin/menu/bulk-delete', methods=['POST'])
def bulk_delete_menu():
    data = request.json
    item_ids = data.get('ids', [])
    if not item_ids:
        return jsonify({"success": False, "message": "No item IDs provided"}), 400
    
    success, message = delete_menu_items_bulk(item_ids)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400

@menu_bp.route('/api/admin/menu/<item_id>', methods=['DELETE'])
def remove_item(item_id):
    success, message = delete_menu_item(item_id)
    return jsonify({"success": success, "message": message})

@menu_bp.route('/api/admin/menu/<item_id>/toggle', methods=['POST'])
def toggle_status(item_id):
    success, message = toggle_availability(item_id)
    return jsonify({"success": success, "message": message})
