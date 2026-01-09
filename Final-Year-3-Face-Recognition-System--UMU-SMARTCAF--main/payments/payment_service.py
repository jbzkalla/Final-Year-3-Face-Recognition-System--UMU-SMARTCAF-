import os
import uuid
import datetime
from utils.constants import DATA_DIR
from data.file_manager import read_json, write_json

PAYMENTS_DB_FILE = os.path.join(DATA_DIR, "payments.json")

def get_all_payments():
    """
    Returns all registered payments from the JSON database.
    """
    return read_json(PAYMENTS_DB_FILE, default=[])

def get_payment_stats():
    """
    Calculates summary statistics for the dashboard.
    """
    payments = get_all_payments()
    
    total_users = len(set(p.get('user_id') for p in payments))
    paid_count = len([p for p in payments if str(p.get('status')).lower() == 'paid'])
    unpaid_count = len([p for p in payments if str(p.get('status')).lower() == 'unpaid'])
    
    revenue = 0
    for p in payments:
        if str(p.get('status')).lower() == 'paid':
            try:
                amt = float(str(p.get('amount', 0)).replace(',', ''))
                revenue += amt
            except:
                pass
    
    return {
        "total_users": total_users,
        "paid_users": paid_count,
        "unpaid_users": unpaid_count,
        "revenue": revenue,
        "pending_invoices": unpaid_count,
        "total_revenue": revenue
    }

def get_payment_by_id(payment_id):
    """
    Finds a specific payment record by its unique ID.
    """
    payments = get_all_payments()
    for p in payments:
        if p.get('id') == payment_id:
            return p
    return None

def create_payment(data):
    """
    Saves a new payment record to the database.
    Required fields in data: user_id, user_name, amount, status
    """
    payments = get_all_payments()
    
    new_payment = {
        "id": data.get('id') or f"PAY-{os.urandom(4).hex().upper()}",
        "user_id": data.get('user_id'),
        "user_name": data.get('user_name', 'Unknown'),
        "amount": float(str(data.get('amount', 0)).replace(',', '')),
        "date": data.get('date') or datetime.datetime.now().strftime("%Y-%m-%d"),
        "meal_type": data.get('meal_type', 'Full Day'),
        "status": data.get('status', 'Paid'),
        "method": data.get('method', 'Manual Entry'),
        "description": data.get('description', ''),
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    payments.append(new_payment)
    if write_json(PAYMENTS_DB_FILE, payments):
        return new_payment
    return None

def update_payment_status(payment_id, status):
    """
    Updates the status of an existing payment record.
    """
    payments = get_all_payments()
    updated_record = None
    
    for p in payments:
        if p.get('id') == payment_id:
            p['status'] = status
            p['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_record = p
            break
            
    if updated_record:
        write_json(PAYMENTS_DB_FILE, payments)
        return updated_record
    return None

def delete_payment(payment_id):
    """
    Removes a payment record from the database.
    """
    payments = get_all_payments()
    initial_len = len(payments)
    payments = [p for p in payments if p.get('id') != payment_id]
    
    if len(payments) < initial_len:
        if write_json(PAYMENTS_DB_FILE, payments):
            return True
    return False

def get_user_payments(user_id):
    """
    Returns all payment records for a specific user ID.
    """
    payments = get_all_payments()
    return [p for p in payments if p.get('user_id') == user_id]
