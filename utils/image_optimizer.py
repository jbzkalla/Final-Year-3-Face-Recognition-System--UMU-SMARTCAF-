import os
import io
import time
import base64
from PIL import Image

MAX_SIZE = (1024, 1024)
QUALITY = 80

def optimize_image_file(file_storage, output_dir, filename_prefix):
    """
    Optimizes a Flask FileStorage object:
    - Resizes to max 1024x1024
    - Converts to WebP
    - Saves to output_dir
    Returns the relative path or filename of the saved file.
    """
    try:
        # Open image from stream
        img = Image.open(file_storage.stream)
        
        # Convert to RGB (in case of RGBA/P mode which JPEG/WebP might struggle with, 
        # though WebP supports transparency, it's safer to standardize if needed. 
        # For WebP transparency is fine, so we keep RGBA if present, providing fallback for RGB)
        if img.mode in ('P', 'CMYK'):
            img = img.convert('RGB')
            
        # Resize if necessary
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        
        # Generate filename
        # Clean the prefix and ensure unique name
        timestamp = int(time.time())
        clean_prefix = str(filename_prefix).replace(" ", "_")
        filename = f"{clean_prefix}_{timestamp}.webp"
        save_path = os.path.join(output_dir, filename)
        
        # Create directory if it doesn't exist (handled by caller usually but good safety)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save as WebP
        img.save(save_path, 'WEBP', quality=QUALITY, optimize=True)
        
        return filename
    except Exception as e:
        print(f"Error optimizing image: {e}")
        # Fallback: maintain original behavior if optimization fails? 
        # Or re-raise. Let's return None to signal failure.
        return None

def optimize_base64_image(base64_string, output_dir, filename_prefix):
    """
    Optimizes a Base64 encoded image string:
    - Decodes base64
    - Resizes to max 1024x1024
    - Converts to WebP
    - Saves to output_dir
    Returns the absolute path of the saved file.
    """
    try:
        if ',' in base64_string:
            header, encoded = base64_string.split(',', 1)
        else:
            encoded = base64_string

        image_data = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(image_data))
        
        if img.mode in ('P', 'CMYK'):
            img = img.convert('RGB')
            
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        
        timestamp = int(time.time())
        clean_prefix = str(filename_prefix).replace(" ", "_")
        filename = f"{clean_prefix}_{timestamp}.webp"
        save_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        img.save(save_path, 'WEBP', quality=QUALITY, optimize=True)
        
        return save_path
    except Exception as e:
        print(f"Error optimizing base64 image: {e}")
        return None
