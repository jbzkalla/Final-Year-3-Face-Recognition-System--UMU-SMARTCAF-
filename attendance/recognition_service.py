import cv2
import numpy as np
import os
import base64

# Global recognizer instance
RECOGNIZER = None
LABEL_MAP = {} # Map ID to User ID (if needed, or just use ID directly)

def load_model():
    global RECOGNIZER, LABEL_MAP
    try:
        # Check if model exists
        model_path = "data/trainer.yml"
        if not os.path.exists(model_path):
            print("Model not found at", model_path)
            return False
            
        RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
        RECOGNIZER.read(model_path)
        
        # Load labels
        import json
        labels_path = "data/labels.json"
        if os.path.exists(labels_path):
            with open(labels_path, 'r') as f:
                LABEL_MAP = json.load(f)
        
        print("Model and labels loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def recognize_face(image_data):
    """
    Recognize face from base64 image data.
    Returns: (user_id, confidence) or (None, 0)
    """
    global RECOGNIZER
    if RECOGNIZER is None:
        # Try loading
        if not load_model():
            return None, 0

    try:
        # Decode base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Detect face (assuming the image sent is already a face or contains one)
        # For better results, we should run face detection here too
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        
        for (x, y, w, h) in faces:
            # Standardize face size for prediction (Must match training size)
            face_roi = img[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (200, 200))
            
            # Predict
            id_, confidence = RECOGNIZER.predict(face_resized)
            
            # Confidence: 0 is perfect match, usually < 50 is good match
            # We convert it to a percentage-like score where 100 is best
            # LBPH confidence is distance, so lower is better.
            # Let's say < 50 is a match.
            
            if confidence < 60: # Threshold
                confidence_score = round(100 - confidence)
                # Map integer ID to string ID
                real_user_id = LABEL_MAP.get(str(id_), str(id_))
                return real_user_id, confidence_score
            else:
                return None, round(100 - confidence) # Unknown
                
        return None, 0 # No face found
        
    except Exception as e:
        print(f"Recognition error: {e}")
        return None, 0
