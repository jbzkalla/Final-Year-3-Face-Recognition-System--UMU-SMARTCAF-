from attendance.attendance_service import get_attendance_records
from users.user_service import get_user_by_id
from datetime import datetime, timedelta

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
        log_time = log.get('Time')
        if not log_date:
            continue
            
        if log_date < start_date or log_date > end_date:
            continue
            
        # User ID filtering
        id_in_log = log.get('User ID')
        if user_id and str(id_in_log) != str(user_id):
            continue
            
        # Meal filtering (Assuming 'Status' might contain meal info or we skip this for now)
        # In a real system, we'd store the session/meal type in the log.
        # For now, we'll just pass through if meal_type is 'all' or not specified.
        if meal_type and meal_type != 'all':
             # Placeholder: If we stored meal type, we'd check it here.
             pass
            
        # Department filtering (Mocking department check)
        
        # Fetch user details
        user_id = log.get('User ID')
        user = get_user_by_id(user_id)
        user_name = user['name'] if user else f"User {user_id}"

        # Standardize log format for frontend
        formatted_log = {
            "id": user_id,
            "name": user_name,
            "timestamp": f"{log_date} {log_time}",
            "date": log_date,
            "time": log_time,
            "session": "General", # Placeholder session
            "status": log.get('Status')
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
