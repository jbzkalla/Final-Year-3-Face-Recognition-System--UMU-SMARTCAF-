import cv2
import numpy as np
import os
import json
import shutil
from deepface import DeepFace
from utils.constants import (
    DATA_DIR, IMAGES_DIR, EMBEDDINGS_FILE, 
    USERS_DB_FILE, MAX_EMBEDDINGS_PER_USER,
    OUTLIER_THRESHOLD, FRAME_WIDTH, FRAME_HEIGHT,
    BLUR_THRESHOLD
)

from utils.image_processing import get_blur_score, preprocess_image

def train_model(progress_callback=None):
    """
    Optimized training pipeline:
    1. Preprocesses images (resize).
    2. Fetches metadata (name, role).
    3. Extracts multiple clean embeddings (multi-vector support).
    4. Removes outliers.
    5. Cleans up excess images.
    Returns: (success, message)
    """
    if progress_callback:
        progress_callback(10, "Initializing training pipeline...")

    if not os.path.exists(IMAGES_DIR):
        return False, "No images directory found."

    if progress_callback:
        progress_callback(15, "Loading user metadata...")

    # Load User Metadata for JSON profiling
    user_metadata = {}
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, 'r') as f:
                users_list = json.load(f)
                user_metadata = {u['id']: u for u in users_list}
        except Exception as e:
            print(f"Warning: Could not load user metadata: {e}")

    # Initialize or Load Master Embeddings Cache
    master_embeddings = {}
    
    # Traverse user directories
    user_folders = [f for f in os.listdir(IMAGES_DIR) if os.path.isdir(os.path.join(IMAGES_DIR, f))]
    
    if not user_folders:
        return False, "No user data found to process."

    processed_count = 0
    total_images_removed = 0
    total_users = len(user_folders)

    for i, user_id in enumerate(user_folders):
        user_folder_path = os.path.join(IMAGES_DIR, user_id)
        image_files = [f for f in os.listdir(user_folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
        
        if progress_callback:
            current_progress = 15 + int((i / total_users) * 75)
            progress_callback(current_progress, f"Optimizing profile for {user_id}...")

        if not image_files:
            continue

        valid_image_data = [] # List of (path, embedding, name)

        print(f"Optimizing identity for {user_id} ({len(image_files)} images)...")

        for img_name in image_files:
            img_path = os.path.join(user_folder_path, img_name)
            try:
                # 1. PREPROCESSING: Resize image to consolidate feature extraction load
                img = cv2.imread(img_path)
                if img is None: continue
                
                # Standardize resolution (640x480)
                img_resized = cv2.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))
                
                # ── QUALITY CHECK: Blur Detection ──
                if get_blur_score(img_resized) < BLUR_THRESHOLD:
                    continue
                
                # ── PREPROCESSING: Illumination Normalization ──
                img_normalized = preprocess_image(img_resized)
                
                # 2. FEATURE EXTRACTION (Facenet + MTCNN)
                # We extract multiple variations (Augmentation) to improve robustness
                variations = [img_normalized]
                
                # Add synthetic variations for lighting/contrast
                # Higher contrast
                alpha = 1.2; beta = 10
                variations.append(cv2.convertScaleAbs(img_normalized, alpha=alpha, beta=beta))
                # Slightly darker
                variations.append(cv2.convertScaleAbs(img_normalized, alpha=0.8, beta=-10))

                for v_img in variations:
                    try:
                        results = DeepFace.represent(
                            img_path=v_img, 
                            model_name="Facenet", 
                            detector_backend="mtcnn",
                            enforce_detection=True,
                            align=True
                        )
                        
                        if results:
                            embedding = results[0]["embedding"]
                            valid_image_data.append({
                                "embedding": embedding,
                                "name": img_name
                            })
                    except:
                        continue
            except Exception as e:
                # Skip if no face found
                continue

        if not valid_image_data:
            print(f"Warning: No valid faces found for {user_id}.")
            continue

        # --- MULTI-VECTOR OUTLIER REMOVAL ---
        embeddings_arr = np.array([d["embedding"] for d in valid_image_data])
        mean_embedding = np.mean(embeddings_arr, axis=0)

        # Calculate distances to mean
        distances = [np.linalg.norm(np.array(d["embedding"]) - mean_embedding) for d in valid_image_data]
        
        # Calculate cleanup threshold
        dist_mean = np.mean(distances)
        dist_std = np.std(distances)
        threshold = dist_mean + (OUTLIER_THRESHOLD * dist_std) if len(distances) > 3 else 999
        
        # Filter and Score
        clean_data = []
        for i, d in enumerate(valid_image_data):
            if distances[i] <= threshold:
                d["dist_from_mean"] = distances[i]
                clean_data.append(d)

        # Sort by distance from mean (lower is mejor/cleaner)
        clean_data.sort(key=lambda x: x["dist_from_mean"])
        
        # Keep top N embeddings (Multi-embedding support)
        # We store multiple vectors instead of one average for higher accuracy
        final_embeddings = [d["embedding"] for d in clean_data[:MAX_EMBEDDINGS_PER_USER]]
        
        # Fetch metadata
        meta = user_metadata.get(user_id, {})
        
        # Store in Optimized JSON Format
        master_embeddings[user_id] = {
            "name": meta.get("name", "Unknown User"),
            "role": meta.get("role", "student"),
            "embeddings": final_embeddings
        }

        # --- STORAGE CLEANUP ---
        # Keep only the images corresponding to the stored embeddings
        keep_names = set(d["name"] for d in clean_data[:MAX_EMBEDDINGS_PER_USER])
        for img_name in image_files:
            if img_name not in keep_names:
                try:
                    os.remove(os.path.join(user_folder_path, img_name))
                    total_images_removed += 1
                except:
                    pass

        processed_count += 1

    # Final Save to Optimized Master File
    if progress_callback:
        progress_callback(95, "Finalizing identity cluster...")
        
    try:
        with open(EMBEDDINGS_FILE, 'w') as f:
            json.dump(master_embeddings, f, indent=4)
            
        # Refresh global cache immediately if in the same process
        try:
            from attendance.recognition_service import refresh_embeddings_cache
            refresh_embeddings_cache()
        except:
            pass

        return True, f"Optimization Complete! {processed_count} profiles updated. {total_images_removed} redundant images purged."
    except Exception as e:
        return False, f"Failed to finalize embeddings: {str(e)}"

if __name__ == '__main__':
    def print_progress(percent, msg):
        print(f"[{percent}%] {msg}")
    success, msg = train_model(progress_callback=print_progress)
    print(msg)
