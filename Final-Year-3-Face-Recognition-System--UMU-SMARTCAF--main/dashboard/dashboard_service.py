from utils.constants import USERS_DB_FILE
from data.file_manager import read_json

def get_dashboard_stats():
    """
    Aggregates statistics for the dashboard.
    """
    from datetime import datetime
    
    import os
    import csv
    from utils.constants import ATTENDANCE_FILE, DATA_DIR, BASE_DIR
    
    users = read_json(USERS_DB_FILE, default=[])
    total_users = len(users)
    
    # 1. Real-time Attendance Count
    # Start with 0
    todays_attendance = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(ATTENDANCE_FILE):
        try:
            with open(ATTENDANCE_FILE, 'r') as f:
                reader = csv.DictReader(f)
                unique_attendees = set()
                for row in reader:
                    if row.get('Date') == today_str:
                         unique_attendees.add(row.get('User ID'))
                todays_attendance = len(unique_attendees)
        except Exception as e:
            print(f"Error reading attendance: {e}")

    # 2. Real-time Paid vs Unpaid Chart Logic
    from payments.payment_service import get_payment_stats
    pay_stats = get_payment_stats()
    
    paid_count = pay_stats['paid_users']
    unpaid_count = pay_stats['unpaid_users']
    total_records = paid_count + unpaid_count
    
    if total_records > 0:
        paid_percentage = int((paid_count / total_records) * 100)
        unpaid_percentage = 100 - paid_percentage
    else:
        paid_percentage = 0
        unpaid_percentage = 0

    
    # Real-time Meal Session Logic
    now = datetime.now()
    hour = now.hour
    
    current_meal = "Closed"
    if 6 <= hour < 9:
        current_meal = "Breakfast"
    elif 12 <= hour < 14:
        current_meal = "Lunch"
    elif 18 <= hour < 21:
        current_meal = "Supper"
    
    return {
        "total_users": total_users,
        "todays_attendance": todays_attendance,
        "paid_percentage": paid_percentage,
        "unpaid_percentage": unpaid_percentage,
        "current_meal": current_meal,
        "payment_counts": {"paid": paid_count, "unpaid": unpaid_count} # Optional breakdown
    }

def get_recent_notifications():
    """
    Generates notifications based on real system data.
    """
    from datetime import datetime, timedelta
    import csv
    import os
    import shutil
    from utils.constants import ATTENDANCE_FILE, MODELS_DIR, DATA_DIR
    
    notifications = []
    now = datetime.now()
    
    # 1. Check for new users in the last 24 hours
    users = read_json(USERS_DB_FILE, default=[])
    total_users = len(users)
    one_day_ago = now - timedelta(days=1)
    
    new_users_count = 0
    for user in users:
        try:
            created_at = datetime.strptime(user.get('created_at', ''), "%Y-%m-%d %H:%M:%S")
            if created_at > one_day_ago:
                new_users_count += 1
        except:
            pass
            
    if new_users_count > 0:
        notifications.append({
            "icon": "ri-user-add-line",
            "text": f"{new_users_count} new users registered in the last 24 hours.",
            "time": "Recent",
            "type": "info"
        })
    
    # 2. Attendance Monitor
    today_str = now.strftime("%Y-%m-%d")
    today_attendance_count = 0
    if os.path.exists(ATTENDANCE_FILE):
        try:
            with open(ATTENDANCE_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Date') == today_str:
                        today_attendance_count += 1
        except:
            pass
            
    if today_attendance_count == 0 and now.hour >= 9:
         notifications.append({
            "icon": "ri-calendar-event-line",
            "text": "No attendance recorded yet today.",
            "time": "Today",
            "type": "warning"
        })
    elif today_attendance_count > 0:
        notifications.append({
            "icon": "ri-check-double-line",
            "text": f"Attendance active: {today_attendance_count} check-ins today.",
            "time": "Today",
            "type": "success"
        })
        
    # 3. Model Status (Trainer)
    trainer_path = os.path.join(DATA_DIR, 'trainer.yml')
    if os.path.exists(trainer_path):
        mtime = os.path.getmtime(trainer_path)
        last_trained = datetime.fromtimestamp(mtime)
        time_diff = now - last_trained
        
        if time_diff.days > 7:
             notifications.append({
                "icon": "ri-brain-line",
                "text": "Face recognition model hasn't been trained in over a week.",
                "time": f"{time_diff.days} days ago",
                "type": "warning"
            })
        else:
             notifications.append({
                "icon": "ri-brain-line",
                "text": "Recognition model is up to date.",
                "time": "Recently",
                "type": "success"
            })
    else:
        notifications.append({
            "icon": "ri-alarm-warning-line",
            "text": "Recognition model not found. Please train the system.",
            "time": "Create Now",
            "type": "error"
        })

    # 4. Storage Health
    try:
        total, used, free = shutil.disk_usage(DATA_DIR)
        free_gb = free // (2**30)
        if free_gb < 2:
            notifications.append({
                "icon": "ri-hard-drive-2-line",
                "text": f"Low disk space: Only {free_gb}GB remaining.",
                "time": "Critical",
                "type": "error"
            })
        else:
             notifications.append({
                "icon": "ri-server-line",
                "text": "System health check passed.",
                "time": "Just now",
                "type": "success"
            })
    except:
        pass

    return notifications

def get_student_stats(user_id):
    """
    Retrieves statistics specifically for a single student.
    """
    from datetime import datetime
    import os
    import csv
    from utils.constants import ATTENDANCE_FILE, USERS_DB_FILE
    from payments.payment_service import get_user_payments
    
    # Get user details for profile
    users = read_json(USERS_DB_FILE, default=[])
    user_detail = next((u for u in users if u['id'] == user_id), {})

    # 1. Individual Attendance & History
    total_meals = 0
    history = []
    if os.path.exists(ATTENDANCE_FILE):
        try:
            with open(ATTENDANCE_FILE, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for row in rows:
                    if row.get('User ID') == user_id:
                        total_meals += 1
                        history.append({
                            "date": row.get('Date'),
                            "time": row.get('Time'),
                            "session": row.get('Session', 'N/A'),
                            "status": "Verified"
                        })
                # Sort history by date/time (reverse) and take last 5
                # For simplicity, assuming file is chronological
                history = history[-5:][::-1]
        except:
            pass
            
    # 2. Financial Status
    payments = get_user_payments(user_id)
    status = "Unpaid"
    amount_paid = 0
    if payments:
        latest = payments[-1]
        status = latest.get('status', 'Unpaid')
        amount_paid = latest.get('amount', 0)
        
    hour = datetime.now().hour
    current_meal = "Closed"
    if 6 <= hour < 9: current_meal = "Breakfast"
    elif 12 <= hour < 14: current_meal = "Lunch"
    elif 18 <= hour < 21: current_meal = "Supper"

    return {
        "is_student": True,
        "total_meals": total_meals,
        "payment_status": status,
        "current_balance": f"UGX {amount_paid:,}",
        "current_meal": current_meal,
        "profile": {
            "name": user_detail.get('name', 'N/A'),
            "id": user_detail.get('id', 'N/A'),
            "dept": user_detail.get('department', 'General'),
            "email": user_detail.get('email', 'N/A')
        },
        "history": history
    }
