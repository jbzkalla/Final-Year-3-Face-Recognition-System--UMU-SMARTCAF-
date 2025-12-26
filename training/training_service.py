import threading
from training.model_manager import train_model
from auth.password_utils import verify_password
# Mock admin password for now, or fetch from config/env
ADMIN_PASSWORD_HASH = "..." # We'll use a simple check or integrate with auth service

# Global state
TRAINING_STATE = {
    "status": "idle", # idle, training, completed, error
    "message": "",
    "progress": 0
}

def authenticate_training(password):
    # In a real app, check against admin user's password
    # For this demo, hardcode 'admin123' or check a specific logic
    # Let's assume we use the same auth service logic or a specific training password
    # For simplicity:
    return password == "admin123"

def start_training_thread():
    global TRAINING_STATE
    if TRAINING_STATE['status'] == 'training':
        return False, "Training already in progress"
        
    TRAINING_STATE['status'] = 'training'
    TRAINING_STATE['message'] = 'Starting training...'
    TRAINING_STATE['progress'] = 10
    
    thread = threading.Thread(target=_run_training)
    thread.start()
    return True, "Training started"

def _run_training():
    global TRAINING_STATE
    try:
        TRAINING_STATE['progress'] = 30
        TRAINING_STATE['message'] = 'Processing images...'
        
        success, msg = train_model()
        
        if success:
            TRAINING_STATE['progress'] = 100
            TRAINING_STATE['status'] = 'completed'
            TRAINING_STATE['message'] = msg
        else:
            TRAINING_STATE['progress'] = 0
            TRAINING_STATE['status'] = 'error'
            TRAINING_STATE['message'] = msg
            
    except Exception as e:
        TRAINING_STATE['status'] = 'error'
        TRAINING_STATE['message'] = str(e)

def get_training_status():
    return TRAINING_STATE
