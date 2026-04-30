import cv2
import time

def get_camera(index=0):
    """
    Initializes and returns a camera object.
    """
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {index}")
        return None
    return cap

def release_camera(cap):
    """
    Releases the camera resource.
    """
    if cap:
        cap.release()

def capture_frame(cap):
    """
    Captures a single frame from the camera.
    Returns (success, frame).
    """
    if not cap or not cap.isOpened():
        return False, None
    
    ret, frame = cap.read()
    return ret, frame

def get_available_cameras(max_cameras=5):
    """
    Checks for available cameras and returns a list of indices.
    """
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras
