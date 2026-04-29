import os
import base64
import time
import cv2
import numpy as np
from utils.image_processing import get_blur_score
from utils.constants import BLUR_THRESHOLD

DATA_DIR = "data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def create_user_folder(user_id):
    """
    Creates a folder for a specific user's images.
    """
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def save_face_image(user_id, image_data):
    """
    Saves a base64 encoded image to the user's folder.
    """
    try:
        user_folder = create_user_folder(user_id)
        
        # ── QUALITY CHECK: Blur Detection ──
        encoded_data = image_data.split(',')[1] if ',' in image_data else image_data
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is not None:
            blur_score = get_blur_score(img)
            if blur_score < BLUR_THRESHOLD:
                return False, f"Image too blurry (Score: {blur_score:.1f}). Please stay still."

        from utils.image_optimizer import optimize_base64_image
        
        # Optimize and save as WebP
        result_path = optimize_base64_image(image_data, user_folder, user_id)
        
        if result_path:
            return True, result_path
        else:
            return False, "Failed to optimize and save image"
    except Exception as e:
        return False, str(e)

def has_face_data(user_id):
    """
    Checks if a user has any face images saved OR an identity vector in embeddings.json.
    """
    # 1. Check images
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    has_images = False
    if os.path.exists(user_folder):
        try:
            has_images = len(os.listdir(user_folder)) > 0
        except:
            pass
            
    if has_images:
        return True
        
    # 2. Check embeddings
    from utils.constants import EMBEDDINGS_FILE
    import json
    if os.path.exists(EMBEDDINGS_FILE):
        try:
            with open(EMBEDDINGS_FILE, 'r') as f:
                embeddings = json.load(f)
                return str(user_id) in embeddings
        except:
            return False
            
    return False
