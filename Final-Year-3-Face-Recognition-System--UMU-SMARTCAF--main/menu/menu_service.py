import os
import uuid
import json
from datetime import datetime
from data.file_manager import read_json, write_json

# File paths
MENU_FILE = "data/menu.json"
IMAGE_DIR = "data/menu_images"
AUDIT_LOG_FILE = "data/audit_logs.json"

# Ensure directories and files exist
for path in [IMAGE_DIR, "data"]:
    if not os.path.exists(path):
        os.makedirs(path)

for file in [MENU_FILE, AUDIT_LOG_FILE]:
    if not os.path.exists(file):
        write_json(file, [])

def log_action(user_email, action, details):
    """Logs administrative actions for accountability."""
    logs = read_json(AUDIT_LOG_FILE)
    new_log = {
        "timestamp": datetime.now().isoformat(),
        "user": user_email,
        "action": action,
        "details": details
    }
    logs.append(new_log)
    write_json(AUDIT_LOG_FILE, logs)

def get_all_menu_items():
    return read_json(MENU_FILE)

def get_menu_by_date(date_str):
    all_items = read_json(MENU_FILE)
    return [item for item in all_items if item.get('date') == date_str]

def add_menu_item(data, image_file=None):
    items = read_json(MENU_FILE)
    
    item_id = str(uuid.uuid4())
    image_path = "static/images/default-meal.png"

    if image_file:
        from utils.image_optimizer import optimize_image_file
        # Use item_id as prefix
        optimized_filename = optimize_image_file(image_file, IMAGE_DIR, item_id)
        if optimized_filename:
            image_path = f"data/menu_images/{optimized_filename}"
        else:
            # Fallback if optimization fails (though it shouldn't)
            # We can log error, but for now fallback to raw save or skip?
            # Let's fallback to original raw save if optimization returns None
            filename = f"{item_id}_{image_file.filename}"
            save_path = os.path.join(IMAGE_DIR, filename)
            image_file.save(save_path)
            image_path = f"data/menu_images/{filename}"

    new_item = {
        "id": item_id,
        "name": data.get('name'),
        "category": data.get('category'), # Meal, Drink, Snack
        "description": data.get('description', ''),
        "image_path": image_path,
        "price": int(data.get('price', 0)),
        "ratings": {"likes": 0, "dislikes": 0},
        "time_served": data.get('time_served'), # Breakfast, Lunch, Supper
        "date": data.get('date', datetime.now().strftime('%Y-%m-%d')),
        "is_available": data.get('is_available', True),
        "created_at": datetime.now().isoformat()
    }
    
    items.append(new_item)
    write_json(MENU_FILE, items)
    
    # Audit log
    from flask import session
    user = session.get('user', {})
    log_action(user.get('email', 'System'), "ADD_MEAL", f"Added {new_item['name']} (ID: {item_id})")
    
    return True, "Item added successfully", new_item

def update_menu_item(item_id, data, image_file=None):
    items = read_json(MENU_FILE)
    for item in items:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['category'] = data.get('category', item['category'])
            item['description'] = data.get('description', item['description'])
            item['price'] = int(data.get('price', item.get('price', 0)))
            item['time_served'] = data.get('time_served', item['time_served'])
            item['date'] = data.get('date', item['date'])
            item['is_available'] = data.get('is_available', item['is_available'])
            
            if image_file:
                # Delete old image if it's not the default
                if item['image_path'] and "default-meal" not in item['image_path']:
                    old_path = item['image_path']
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except: pass
                
                from utils.image_optimizer import optimize_image_file
                optimized_filename = optimize_image_file(image_file, IMAGE_DIR, item_id)
                
                if optimized_filename:
                    item['image_path'] = f"data/menu_images/{optimized_filename}"
                else:
                    # Fallback
                    filename = f"{item_id}_{image_file.filename}"
                    save_path = os.path.join(IMAGE_DIR, filename)
                    image_file.save(save_path)
                    item['image_path'] = f"data/menu_images/{filename}"
                
            write_json(MENU_FILE, items)
            
            # Audit log
            from flask import session
            user = session.get('user', {})
            log_action(user.get('email', 'System'), "UPDATE_MEAL", f"Updated {item['name']} (ID: {item_id})")
            
            return True, "Item updated successfully"
            
    return False, "Item not found"

def delete_menu_item(item_id):
    items = read_json(MENU_FILE)
    for i, item in enumerate(items):
        if item['id'] == item_id:
            # Delete image
            if item['image_path'] and "default-meal" not in item['image_path']:
                if os.path.exists(item['image_path']):
                    try: os.remove(item['image_path'])
                    except: pass
            
            items.pop(i)
            write_json(MENU_FILE, items)
            
            # Audit log
            from flask import session
            user = session.get('user', {})
            log_action(user.get('email', 'System'), "DELETE_MEAL", f"Deleted meal ID: {item_id}")
            
            return True, "Item deleted successfully"
            
    return False, "Item not found"

def toggle_availability(item_id):
    items = read_json(MENU_FILE)
    for item in items:
        if item['id'] == item_id:
            item['is_available'] = not item.get('is_available', True)
            write_json(MENU_FILE, items)
            return True, f"Status changed to {'Available' if item['is_available'] else 'Finished'}"
    return False, "Item not found"

def vote_on_item(item_id, vote_type, prev_vote=None):
    """Handles student likes/dislikes for meals with support for swapping choices."""
    items = read_json(MENU_FILE)
    for item in items:
        if item['id'] == item_id:
            if 'ratings' not in item:
                item['ratings'] = {"likes": 0, "dislikes": 0}
            
            # If changing mind, decrement the previous vote
            if prev_vote:
                if prev_vote == 'like' and item['ratings']['likes'] > 0:
                    item['ratings']['likes'] -= 1
                elif prev_vote == 'dislike' and item['ratings']['dislikes'] > 0:
                    item['ratings']['dislikes'] -= 1
            
            # Increment new vote
            if vote_type == 'like':
                item['ratings']['likes'] += 1
            elif vote_type == 'dislike':
                item['ratings']['dislikes'] += 1
                
            write_json(MENU_FILE, items)
            return True, "Vote updated"
    return False, "Item not found"

def bulk_toggle_availability(date_str, time_served, status):
    """Toggles all items for a specific shift (e.g., End of Lunch)."""
    items = read_json(MENU_FILE)
    count = 0
    for item in items:
        # If date_str is provided, filter by it. If not, apply to all items (global close shift).
        date_match = not date_str or item.get('date') == date_str
        time_match = item.get('time_served') == time_served or time_served == 'All'
        
        if date_match and time_match:
            item['is_available'] = status
            count += 1
    
    if count > 0:
        write_json(MENU_FILE, items)
        
        # Audit log
        from flask import session
        user = session.get('user', {})
        log_action(user.get('email', 'System'), "BULK_TOGGLE", f"Set {count} items in {time_served} to {status}")
        
        return True, f"Updated {count} items"
    return False, "No items found to update"
def delete_menu_items_bulk(item_ids):
    """Deletes multiple menu items."""
    items = read_json(MENU_FILE)
    initial_len = len(items)
    items = [i for i in items if i['id'] not in item_ids]
    
    if len(items) < initial_len:
        write_json(MENU_FILE, items)
        
        # Audit log
        from flask import session
        user = session.get('user', {})
        log_action(user.get('email', 'System'), "BULK_DELETE_MENU", f"Deleted {initial_len - len(items)} items")
        
        return True, f"Deleted {initial_len - len(items)} items"
    return False, "No items found to delete"
