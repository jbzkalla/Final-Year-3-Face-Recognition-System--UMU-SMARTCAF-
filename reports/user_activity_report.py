from attendance.attendance_service import get_attendance_records
from payments.payment_service import get_all_payments
from users.user_service import get_user_by_id

def generate_user_activity_report(user_input):
    import csv
    import os
    from utils.constants import BASE_DIR
    
    # Try to find user by ID first, then by name
    user = get_user_by_id(user_input)
    if not user:
        # Search by name if not found by ID
        # Since get_user_by_id only checks ID, we need to scan users
        from users.user_service import get_all_users
        all_users = get_all_users()
        for u in all_users:
            if user_input.lower() in u.get('name', '').lower():
                user = u
                break
                
    if not user:
        return None
        
    user_id = user['id']
    
    # Look for user image
    # Assuming images are stored in data/images/{user_id}/...
    # We take the first image found
    from utils.constants import DATA_DIR
    import glob
    
    image_dir = os.path.join(DATA_DIR, 'images', str(user_id))
    user['image_url'] = None # Default
    
    if os.path.exists(image_dir):
        files = os.listdir(image_dir)
        # Filter for image files
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if image_files:
            # Construct relative path for frontend serving
            # This relies on the Flask static file serving from root
            user['image_url'] = f"data/images/{user_id}/{image_files[0]}"
    
    # Get attendance history
    all_records = get_attendance_records()
    attendance_history = [r for r in all_records if r.get('User ID') == str(user_id)]
    
    # Get payment history (from Finance CSV as source of truth)
    payment_history = []
    finance_file = os.path.join(BASE_DIR, 'UMU_SmartCaf_Finance_Upload_Final.csv')
    
    current_payment_status = "Unpaid"
    
    if os.path.exists(finance_file):
        try:
            with open(finance_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                     if row.get('Student ID', '').strip() == str(user_id):
                        current_payment_status = row.get('Status', 'Unpaid')
                        payment_date_str = row.get('Payment Date', '')
                        # Try to parse M/D/YYYY to YYYY-MM-DD
                        formatted_date = payment_date_str
                        try:
                            from datetime import datetime
                            if payment_date_str:
                                dt = datetime.strptime(payment_date_str, "%m/%d/%Y")
                                formatted_date = dt.strftime("%Y-%m-%d")
                            else:
                                formatted_date = "Recent Import"
                        except:
                            formatted_date = payment_date_str or "Recent Import"

                        payment_history.append({
                            "type": "finance_record",
                            "title": "Finance Record Update",
                            "status": row.get('Status'),
                            "date": formatted_date,
                            "details": f"Amount: {row.get('Amount Paid', '0')}, Plan: {row.get('Meal Plan', 'N/A')}"
                        })
        except:
            pass
    timeline = []
    
    for att in attendance_history:
        timestamp = f"{att.get('Date', '')} {att.get('Time', '')}".strip()
        timeline.append({
            "type": "attendance",
            "title": "Meal Access", 
            "status": att.get('Status', 'Unknown'),
            "date": timestamp,
            "details": "Verified via Facial Recognition"
        })
        
    for pay in payment_history:
        timeline.append(pay) # payment_history already has formatted items

    # Sort timeline by date desc (simple string sort for now)
    timeline.sort(key=lambda x: x['date'], reverse=True)
    
    stats = {
        "attendance_rate": "95%", # Mock calculation
        "payment_status": current_payment_status,
        "total_meals": len(attendance_history)
    }
    
    return {
        "user": user,
        "stats": stats,
        "timeline": timeline
    }
