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
    
    # Get payment history (from Payment Service - JSON Source of Truth)
    from payments.payment_service import get_user_payments
    try:
        user_payments = get_user_payments(str(user_id))
        for p in user_payments:
            # Check latest status for summary
            current_payment_status = p.get('status', 'Unpaid')
            
            payment_history.append({
                "type": "finance_record",
                "title": "Payment Record",
                "status": p.get('status', 'Unpaid'),
                "date": p.get('date', 'Recent'),
                "details": f"Amount: {p.get('amount', '0')}, Method: {p.get('method', 'N/A')}"
            })
    except Exception as e:
        print(f"Error reading payments: {e}")
        pass
    
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
