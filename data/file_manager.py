import os
import json
import shutil
import datetime

def ensure_directory(path):
    """
    Ensures that a directory exists.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def read_json(path, default=None):
    """
    Reads a JSON file and returns its content.
    Returns default value if file doesn't exist or is invalid.
    """
    if not os.path.exists(path):
        return default if default is not None else {}
        
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {path}: {e}")
        return default if default is not None else {}

def write_json(path, data):
    """
    Writes data to a JSON file atomically.
    """
    try:
        ensure_directory(os.path.dirname(path))
        temp_path = f"{path}.tmp"
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Atomic replace
        if os.path.exists(path):
            os.replace(temp_path, path)
        else:
            os.rename(temp_path, path)
            
        return True
    except Exception as e:
        print(f"Error writing JSON file {path}: {e}", flush=True)
        if os.path.exists(f"{path}.tmp"):
            try:
                os.remove(f"{path}.tmp")
            except:
                pass
        return False

def backup_file(path):
    """
    Creates a backup of the specified file.
    """
    if not os.path.exists(path):
        return False
        
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{path}.{timestamp}.bak"
        shutil.copy2(path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Error backing up file {path}: {e}")
        return False
