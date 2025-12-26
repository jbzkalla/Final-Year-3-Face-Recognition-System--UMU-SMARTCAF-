from flask import Blueprint, request, jsonify
from payments.payment_service import get_all_payments, create_payment, update_payment_status, get_payment_stats, get_payment_by_id
from payments.excel_importer import import_payments_from_file

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/api/payments', methods=['GET'])
def list_payments():
    payments = get_all_payments()
    return jsonify({"success": True, "data": payments})

@payments_bp.route('/api/payments', methods=['POST'])
def add_payment():
    data = request.get_json()
    new_payment = create_payment(data)
    return jsonify({"success": True, "message": "Payment recorded", "data": new_payment}), 201

@payments_bp.route('/api/payments/<payment_id>/status', methods=['PUT'])
def update_status(payment_id):
    data = request.get_json()
    status = data.get('status')
    if not status:
        return jsonify({"success": False, "message": "Status required"}), 400
        
    updated = update_payment_status(payment_id, status)
    if updated:
        return jsonify({"success": True, "message": "Status updated", "data": updated})
    return jsonify({"success": False, "message": "Payment not found"}), 404

@payments_bp.route('/api/payments/stats', methods=['GET'])
def stats():
    stats = get_payment_stats()
    return jsonify({"success": True, "data": stats})

@payments_bp.route('/api/payments/import', methods=['POST'])
def bulk_import():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
        
    if file:
        success, result = import_payments_from_file(file)
        if success:
            # Actually create payments
            count = 0
            for p_data in result:
                create_payment(p_data)
                count += 1
            return jsonify({"success": True, "message": f"Successfully imported {count} records"})
        else:
            return jsonify({"success": False, "message": f"Import failed: {result}"}), 500

@payments_bp.route('/api/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = get_payment_by_id(payment_id)
    if payment:
        return jsonify({"success": True, "data": payment})
    return jsonify({"success": False, "message": "Payment not found"}), 404
