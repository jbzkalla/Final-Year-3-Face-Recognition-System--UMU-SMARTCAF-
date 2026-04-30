import pandas as pd
import os
from data.file_manager import ensure_directory

def read_excel(path):
    """
    Reads an Excel file and returns a list of dictionaries.
    """
    if not os.path.exists(path):
        return []
        
    try:
        df = pd.read_excel(path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error reading Excel file {path}: {e}")
        return []

def write_excel(path, data, columns=None):
    """
    Writes a list of dictionaries to an Excel file.
    """
    try:
        ensure_directory(os.path.dirname(path))
        df = pd.DataFrame(data)
        if columns:
            # Ensure columns exist, fill with empty string if missing
            for col in columns:
                if col not in df.columns:
                    df[col] = ""
            df = df[columns]
            
        df.to_excel(path, index=False)
        return True
    except Exception as e:
        print(f"Error writing Excel file {path}: {e}")
        return False

def append_to_excel(path, data):
    """
    Appends data to an existing Excel file.
    """
    try:
        if os.path.exists(path):
            existing_data = read_excel(path)
            existing_data.extend(data)
            return write_excel(path, existing_data)
        else:
            return write_excel(path, data)
    except Exception as e:
        print(f"Error appending to Excel file {path}: {e}")
        return False
