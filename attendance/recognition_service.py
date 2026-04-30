import cv2
import numpy as np
import os
import base64
import json
import logging
from deepface import DeepFace
from utils.constants import EMBEDDINGS_FILE, RECOGNITION_THRESHOLD, BLUR_THRESHOLD

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global identity vectors (Cached in memory)
EMBEDDINGS_CACHE = {}

# Liveness Tracking
LAST_FACE_CENTER = None
MOTION_THRESHOLD = 2.0 # Pixels of variance needed

def load_embeddings_to_cache():
    """
    MANDATORY: Loads embeddings from JSON into a global NumPy-optimized cache.
    Called once on app startup and whenever data is updated.
    """
    global EMBEDDINGS_CACHE
    try:
        if not os.path.exists(EMBEDDINGS_FILE):
            logger.warning(f"Embeddings file not found at {EMBEDDINGS_FILE}")
            return False
            
        with open(EMBEDDINGS_FILE, 'r') as f:
            raw_data = json.load(f)
        
        new_cache = {}
        for user_id, profile in raw_data.items():
            # Convert list of lists to a single NumPy matrix for vectorized math
            embeddings_list = profile.get("embeddings", [])
            if not embeddings_list: continue
            
            # Ensure they are numpy arrays
            embeddings_matrix = np.array(embeddings_list, dtype=np.float32)
            
            # Normalize embeddings matrix for faster cosine similarity via dot product
            norms = np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
            normalized_matrix = embeddings_matrix / (norms + 1e-8)
            
            new_cache[user_id] = {
                "name": profile.get("name", "Unknown"),
                "role": profile.get("role", "student"),
                "embeddings": normalized_matrix
            }
        
        EMBEDDINGS_CACHE = new_cache
        logger.info(f"Identity cache initialized with {len(EMBEDDINGS_CACHE)} optimized profiles.")
        return True
    except Exception as e:
        logger.error(f"Failed to load identity cache: {e}")
        return False

def refresh_embeddings_cache():
    """
    Updates the in-memory cache manually after registration or training.
    """
    return load_embeddings_to_cache()

from utils.image_processing import get_blur_score, preprocess_image

def recognize_face(image_data):
    """
    Optimized Face Recognition using Multi-Embedding Best-Match Logic.
    Uses Vectorized Cosine Similarity via NumPy.
    Returns: (user_id, confidence_score) or (None, confidence_score)
    """
    global EMBEDDINGS_CACHE
    
    try:
        # 1. Decode base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
             return {
                "user_id": None,
                "confidence": 0,
                "facial_area": None,
                "is_live": False
            }

        # ── QUALITY CHECK: Blur Detection ──
        blur_score = get_blur_score(img)
        if blur_score < BLUR_THRESHOLD:
            logger.warning(f"Recognition skip: Image too blurry (Score: {blur_score:.2f})")
            return {
                "user_id": None,
                "confidence": 0,
                "message": "Too blurry",
                "facial_area": None,
                "is_live": False
            }

        # ── PREPROCESSING: Illumination Normalization ──
        img = preprocess_image(img)

        # 2. Extract Embedding for Most Prominent Face
        try:
            results = DeepFace.represent(
                img_path=img, 
                model_name="Facenet", 
                detector_backend="mtcnn",
                enforce_detection=True,
                align=True
            )
            
            if not results:
                return {
                    "user_id": None,
                    "confidence": 0,
                    "facial_area": None,
                    "is_live": False
                }
                
            input_vector = np.array(results[0]["embedding"], dtype=np.float32)
            # Normalize input vector
            input_vector /= (np.linalg.norm(input_vector) + 1e-8)
            
            # 3. VECTORIZED SIMILARITY SEARCH
            best_user_id = None
            highest_sim = -1.0
            
            # Ensure cache is ready if possible
            if not EMBEDDINGS_CACHE:
                load_embeddings_to_cache()
            
            # Only search if we have data
            if EMBEDDINGS_CACHE:
                for user_id, profile in EMBEDDINGS_CACHE.items():
                    similarities = np.dot(profile["embeddings"], input_vector)
                    best_sim_for_user = np.max(similarities)
                    
                    if best_sim_for_user > highest_sim:
                        highest_sim = best_sim_for_user
                        best_user_id = user_id
            
            # 4. LIVENESS CHECK (Simple Motion Variance)
            global LAST_FACE_CENTER
            facial_area = results[0]["facial_area"]
            current_center = (facial_area['x'] + facial_area['w']/2, facial_area['y'] + facial_area['h']/2)
            
            is_live = True
            if LAST_FACE_CENTER is not None:
                distance = np.sqrt((current_center[0] - LAST_FACE_CENTER[0])**2 + (current_center[1] - LAST_FACE_CENTER[1])**2)
                if distance < MOTION_THRESHOLD: # Check against adjustable variance
                    is_live = False
                    logger.warning("Liveness Check Failed: Static image detected.")
            
            LAST_FACE_CENTER = current_center
            
            # 5. DECISION LOGIC
            confidence = round(highest_sim * 100) if highest_sim > 0 else 0
            
            match_status = "SUCCESS" if highest_sim >= RECOGNITION_THRESHOLD else "FAILURE"
            logger.info(f"Recognition Attempt: User={best_user_id}, Sim={highest_sim:.4f}, Status={match_status}")
            
            if highest_sim >= RECOGNITION_THRESHOLD:
                return {
                    "user_id": best_user_id,
                    "confidence": confidence,
                    "facial_area": facial_area,
                    "is_live": is_live
                }
            else:
                return {
                    "user_id": None,
                    "confidence": confidence,
                    "facial_area": facial_area,
                    "is_live": is_live
                }
                
        except Exception as e:
            # Face not found or representation error
            logger.debug(f"Feature extraction skip: {e}")
            return {
                "user_id": None,
                "confidence": 0,
                "facial_area": None,
                "is_live": False
            }
            
    except Exception as e:
        logger.error(f"Recognition Error: {e}")
        return {
            "user_id": None,
            "confidence": 0,
            "facial_area": None,
            "is_live": False
        }

# Backward compatibility / Initial check
if __name__ == "__main__":
    load_embeddings_to_cache()
