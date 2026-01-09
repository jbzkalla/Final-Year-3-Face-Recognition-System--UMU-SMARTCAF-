from utils.constants import ATTENDANCE_FILE, DATA_DIR, BASE_DIR
from data.file_manager import ensure_directory
from utils.time_utils import get_current_date, get_current_time
from users.user_service import get_user_by_id
import os
import csv

def mark_attendance(user_id, confidence=0):
    """
    Marks attendance for a user.
    Includes logic for Access Granted/Denied based on Payment Status.
    """
    ensure_directory(os.path.dirname(ATTENDANCE_FILE))
    
    date = get_current_date()
    time = get_current_time()
    
    user = get_user_by_id(user_id)
    name = user['name'] if user else "Unknown User"
    
    # Check Payment Status from Database
    from payments.payment_service import get_all_payments
    all_payments = get_all_payments()
    
    # Check if user has any 'Paid' status for current period
    # To be more precise, we check for 'Paid' status in any of their records
    user_payments = [p for p in all_payments if p.get('user_id') == str(user_id)]
    
    payment_status = "Unpaid"
    if any(str(p.get('status')).lower() == 'paid' for p in user_payments):
        payment_status = "Paid"
            
    # Determine Access
    # Granted if 'Paid', otherwise Denied
    access_status = "Granted" if payment_status == "Paid" else "Denied"
    
    # Log to CSV
    try:
        file_exists = os.path.exists(ATTENDANCE_FILE)
        
        # We append every scan, or should we limit to one per session?
        # User requested "Recent Scans", implying a log.
        # Let's log every scan for the "Live" feed, but maybe attendance is unique per day?
        # For "Live Attendance" monitoring, we want to see every attempt.
        
        with open(ATTENDANCE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["User ID", "Name", "Date", "Time", "Status", "Confidence"])
            writer.writerow([user_id, name, date, time, access_status, confidence])
            
        return {
            "success": True, 
            "record": {
                "name": name,
                "status": access_status,
                "confidence": confidence,
                "time": time
            }
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_attendance_records():
    """
    Retrieves all attendance records.
    """
    if not os.path.exists(ATTENDANCE_FILE):
        return []
        
    records = []
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    except:
        pass
    return records

def get_session_stats():
    """
    Calculates statistics for the current active session (Total Scanned, Granted, Denied).
    """
    date = get_current_date()
    records = get_attendance_records()
    
    # Filter for today
    todays_records = [r for r in records if r.get('Date') == date]
    
    total = len(todays_records)
    granted = len([r for r in todays_records if r.get('Status') == 'Granted'])
    denied = len([r for r in todays_records if r.get('Status') == 'Denied'])
    
    return {
        "total": total,
        "granted": granted,
        "denied": denied
    }

def get_recent_logs(limit=10):
    """
    Returns the most recent attendance logs formatted for the frontend.
    """
    records = get_attendance_records()
    # Reverse to get newest first
    recent_raw = records[::-1][:limit]
    
    formatted = []
    for r in recent_raw:
        formatted.append({
            "time": r.get('Time'),
            "name": r.get('Name', 'Unknown'),
            "status": r.get('Status'),
            "confidence": r.get('Confidence', '0')
        })
        
    return formatted
