from utils.constants import AUDIT_LOG_FILE
from data.file_manager import read_json
import datetime
import json
import os
import csv

LOG_FILE = AUDIT_LOG_FILE

def get_logs():
    """
    Retrieves all audit logs.
    """
    return read_json(LOG_FILE, default=[])

def log_event(event_type, user, details, ip_address="Unknown"):
    """
    Logs a security or system event.
    """
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "user": user,
        "details": details,
        "ip_address": ip_address
    }
    
    logs = get_logs()
    logs.insert(0, entry) # Prepend to show newest first
    
    # Keep only last 1000 logs
    if len(logs) > 1000:
        logs = logs[:1000]
        
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
    except Exception as e:
        print(f"Error writing audit log: {e}")

def export_logs_to_csv():
    """
    Exports audit logs to a CSV file and returns the file path.
    """
    logs = get_logs()
    if not logs:
        return None
        
    filename = f"audit_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("data", "reports", filename)
    
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
        
    try:
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Event Type", "User", "Details", "IP Address"])
            for log in logs:
                writer.writerow([
                    log.get("timestamp", ""),
                    log.get("event_type", ""),
                    log.get("user", ""),
                    log.get("details", ""),
                    log.get("ip_address", "")
                ])
        return filepath
    except Exception as e:
        print(f"Error exporting logs: {e}")
        return None
