from attendance.attendance_service import get_attendance_records
from users.user_service import get_user_by_id
from datetime import datetime, timedelta

def _to12h(time_str):
    """Convert HH:MM:SS (24h) to h:MM AM/PM (12h)"""
    if not time_str:
        return time_str
    try:
        t = datetime.strptime(time_str.strip(), '%H:%M:%S')
        return t.strftime('%I:%M %p').lstrip('0')  # e.g. 5:23 PM
    except Exception:
        return time_str

def _infer_meal(time_str):
    """Infer meal from time string HH:MM:SS"""
    if not time_str:
        return None
    try:
        h = int(time_str.split(':')[0])
        if 4 <= h < 11:  return 'breakfast'
        if 11 <= h < 16: return 'lunch'
        if 16 <= h < 23: return 'supper'
    except Exception:
        pass
    return None

def generate_attendance_report(start_date=None, end_date=None, meal_type=None, department=None, user_id=None):
    # Filter logs based on criteria
    filtered_logs = []
    logs = get_attendance_records()
    
    # If no dates provided, default to last 7 days
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
        
    for log in logs:
        # Date filtering
        log_date = log.get('Date')
        log_time = log.get('Time', '')
        if not log_date:
            continue
            
        if log_date < start_date or log_date > end_date:
            continue
            
        # User ID / name filtering — use separate variable to avoid shadowing the filter param
        log_user_id = log.get('User ID')
        # Name is already stored in CSV — no lookup needed for display
        csv_name = log.get('Name', '').strip() or f"User {log_user_id}"

        if user_id and str(log_user_id).lower() != str(user_id).lower():
            # Also try name-based match
            if user_id.lower() not in csv_name.lower():
                continue
            
        # Meal filtering — infer from time
        if meal_type and meal_type != 'all':
            inferred = _infer_meal(log_time)
            if inferred != meal_type.lower():
                continue
        
        # Fetch user details for department (not for name — name comes from CSV)
        user = get_user_by_id(log_user_id)
        department = (user.get('department') or user.get('dept') or '-') if user else '-'

        time_24 = log_time  # raw 24h string
        time_12 = _to12h(log_time)  # 12h formatted

        # Standardize log format for frontend
        formatted_log = {
            "id": log_user_id,
            "name": csv_name,          # Full name from CSV
            "department": department,  # from user profile
            "timestamp": f"{log_date} {time_12}",
            "date": log_date,
            "time": time_12,           # 12-hour format
            "time_raw": time_24,       # kept for meal inference
            "session": "General",
            "status": log.get('Status'),
            "confidence": log.get('Confidence', '-')
        }
        filtered_logs.append(formatted_log)
        
    return filtered_logs

def get_attendance_trends():
    logs = get_attendance_records()
    
    # Last 7 days
    today = datetime.now()
    dates_map = {}
    
    # Initialize last 7 days with 0
    for i in range(6, -1, -1):
        d_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        # We might want day names for the chart labels like 'Mon', 'Tue'
        dates_map[d_str] = 0
        
    for log in logs:
        l_date = log.get('Date')
        if l_date in dates_map:
            dates_map[l_date] += 1
            
    # Convert to labels (Day Name) and data
    labels = []
    data = []
    
    # Sort by date
    for d_str in sorted(dates_map.keys()):
        dt = datetime.strptime(d_str, '%Y-%m-%d')
        labels.append(dt.strftime('%a')) # Mon, Tue...
        data.append(dates_map[d_str])

    return {
        "labels": labels,
        "data": data
    }

def get_meal_distribution():
    logs = get_attendance_records()
    
    # Infer meal from time
    # Breakfast: 04:00 - 11:00
    # Lunch: 11:00 - 16:00
    # Supper: 16:00 - 23:00
    
    distribution = {
        'Breakfast': 0,
        'Lunch': 0,
        'Supper': 0
    }
    
    for log in logs:
        t_str = log.get('Time', '00:00:00')
        try:
            h = int(t_str.split(':')[0])
            if 4 <= h < 11:
                distribution['Breakfast'] += 1
            elif 11 <= h < 16:
                distribution['Lunch'] += 1
            elif 16 <= h < 23:
                distribution['Supper'] += 1
        except:
            pass
            
    return {
        "labels": list(distribution.keys()),
        "data": list(distribution.values())
    }
