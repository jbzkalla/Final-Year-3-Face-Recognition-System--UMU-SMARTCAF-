import cv2
import numpy as np

def get_blur_score(image):
    """
    Calculates the Laplacian variance to estimate image blurriness.
    Higher score = sharper image.
    """
    if image is None:
        return 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def apply_gamma(image, gamma=1.0):
    """Adjusts image brightness using gamma correction."""
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def preprocess_image(image):
    """
    Optimized preprocessing:
    1. Applies adaptive gamma correction for low-light.
    2. Normalizes lighting using CLAHE.
    """
    if image is None:
        return None
        
    # 1. Adaptive Gamma: Brighten if image is too dark
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    
    # If dark (mean < 90), apply brightening gamma
    if mean_brightness < 90:
        gamma_val = 1.5 if mean_brightness < 50 else 1.2
        image = apply_gamma(image, gamma=gamma_val)
    
    # 2. CLAHE Normalization
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    # Merge and convert back to BGR
    limg = cv2.merge((cl,a,b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
