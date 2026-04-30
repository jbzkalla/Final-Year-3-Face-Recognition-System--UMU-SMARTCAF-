from flask import Blueprint, request, jsonify
from support.ticket_service import create_ticket, get_all_tickets, update_ticket_status

support_bp = Blueprint('support', __name__)

@support_bp.route('/api/support/tickets', methods=['GET'])
def list_tickets():
    """
    Endpoint to list all support tickets.
    """
    tickets = get_all_tickets()
    return jsonify({"success": True, "data": tickets})

@support_bp.route('/api/support/tickets/<ticket_id>', methods=['PATCH'])
def update_status(ticket_id):
    """
    Endpoint to update ticket status.
    """
    data = request.json
    if not data or 'status' not in data:
        return jsonify({"success": False, "message": "Missing status field"}), 400
        
    success, message = update_ticket_status(ticket_id, data['status'])
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 404

@support_bp.route('/api/support/tickets', methods=['POST'])
def submit_ticket():
    """
    Endpoint to submit a support ticket.
    """
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    category = data.get('category', 'General')
    ticket_type = data.get('type', 'Feedback')
    
    if not email or not subject or not message:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
        
    success, result = create_ticket(email, subject, message, category, ticket_type)
    
    if success:
        return jsonify({"success": True, "message": "Ticket submitted successfully", "ticket_id": result})
    else:
        return jsonify({"success": False, "message": f"Failed to submit ticket: {result}"}), 500

@support_bp.route('/api/support/info', methods=['GET'])
def system_info():
    """
    Returns basic system information.
    """
    return jsonify({
        "success": True,
        "version": "1.0.0",
        "status": "Operational",
        "support_email": "support@umucanteen.com"
    })
