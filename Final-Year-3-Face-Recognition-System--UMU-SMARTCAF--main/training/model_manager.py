import cv2
import numpy as np
import os
import json

# Paths
DATA_DIR = "data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")
MODEL_PATH = os.path.join(DATA_DIR, "trainer.yml")
LABELS_PATH = os.path.join(DATA_DIR, "labels.json")

def train_model():
    """
    Trains the LBPH face recognizer using images in data/images.
    Returns: (success, message)
    """
    if not os.path.exists(IMAGES_DIR):
        return False, "No images directory found."

    face_samples = []
    ids = []
    label_map = {} # user_id (str) -> label (int)
    current_label = 1
    
    # Initialize detector
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Traverse user directories
    user_folders = [f for f in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, f))]
    
    if not user_folders:
        return False, "No user data found to train."
        
    for user_id in user_folders:
        user_folder_path = os.path.join(IMAGES_DIR, user_id)
        image_paths = [os.path.join(user_folder_path, f) for f in os.listdir(user_folder_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
        
        if not image_paths:
            continue
            
        # Assign label
        label_map[str(current_label)] = user_id # Save as string for JSON
        
        for image_path in image_paths:
            try:
                # Read image in grayscale
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                    
                img_numpy = np.array(img, 'uint8')
                
                # Detect faces (sanity check, though images should be cropped already)
                # If images are already cropped faces, we can skip detection or just use the whole image
                # Assuming face_capture_service saves full frames or cropped? 
                # Usually better to detect again to be sure, or just use the image if it's already a face.
                # Let's assume they are cropped faces for now, or we detect to be safe.
                faces = detector.detectMultiScale(img_numpy)
                
                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        # Standardize face size for LBPH (Critical for accuracy)
                        face_roi = img_numpy[y:y+h, x:x+w]
                        face_resized = cv2.resize(face_roi, (200, 200))
                        face_samples.append(face_resized)
                        ids.append(current_label)
                else:
                    # Fallback: Resize entire image if no face detected
                    face_resized = cv2.resize(img_numpy, (200, 200))
                    face_samples.append(face_resized)
                    ids.append(current_label)
                    
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                
        current_label += 1
        
    if not face_samples:
        return False, "No valid face data found."
        
    # Train
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(face_samples, np.array(ids))
    
    # Save
    recognizer.write(MODEL_PATH)
    
    # Save labels mapping
    with open(LABELS_PATH, 'w') as f:
        json.dump(label_map, f)
        
    return True, f"Model trained with {len(face_samples)} samples from {len(label_map)} users."
