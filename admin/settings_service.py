import json
import os

# Mock settings storage
SETTINGS_FILE = "data/settings.json"
DEFAULT_SETTINGS = {
    "canteen_name": "UMU SmartCaf",
    "operating_year": 2025,
    "confidence_threshold": 75,
    "lockout_duration": 15,
    "max_login_attempts": 3,
    "camera_id": 0,
    "theme": "dark",
    "notifications_enabled": True,
    "enable_2fa": False,
    "liveness_detection": True,
    "spending_limit": 50000,
    "low_balance_warning": 5000,
    "auto_invoicing": True,
    "backup_schedule": "daily",
    "retention_period": 365
}

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)
