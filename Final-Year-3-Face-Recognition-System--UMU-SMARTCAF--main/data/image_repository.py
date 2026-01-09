import os
import base64
import time
import shutil
from data.file_manager import ensure_directory

IMAGES_DIR = "data/images"

def save_image(user_id, image_data):
    """
    Saves a base64 encoded image for a user.
    """
    try:
        user_folder = os.path.join(IMAGES_DIR, str(user_id))
        ensure_directory(user_folder)
        
        # Remove header if present
        if ',' in image_data:
            header, encoded = image_data.split(',', 1)
        else:
            encoded = image_data

        # Decode
        image_bytes = base64.b64decode(encoded)
        
        # Generate filename
        filename = f"{user_id}_{int(time.time())}.jpg"
        filepath = os.path.join(user_folder, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        return True, filepath
    except Exception as e:
        print(f"Error saving image for user {user_id}: {e}")
        return False, str(e)

def get_image_paths(user_id):
    """
    Returns a list of image paths for a user.
    """
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    if not os.path.exists(user_folder):
        return []
        
    images = []
    for filename in os.listdir(user_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images.append(os.path.join(user_folder, filename))
    return images

def delete_user_images(user_id):
    """
    Deletes all images for a user.
    """
    user_folder = os.path.join(IMAGES_DIR, str(user_id))
    if os.path.exists(user_folder):
        try:
            shutil.rmtree(user_folder)
            return True
        except Exception as e:
            print(f"Error deleting images for user {user_id}: {e}")
            return False
    return True
