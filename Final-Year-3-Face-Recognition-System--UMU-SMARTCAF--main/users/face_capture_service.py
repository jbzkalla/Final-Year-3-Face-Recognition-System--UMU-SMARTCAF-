import os
import base64
import time

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
    Checks if a user has any face images saved.
    """
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    if not os.path.exists(user_folder):
        return False
    
    # Check if there are any files in the directory
    try:
        return len(os.listdir(user_folder)) > 0
    except:
        return False
