import os
import pandas as pd
import uuid
import datetime
from werkzeug.utils import secure_filename
from utils.constants import DATA_DIR, USERS_DB_FILE
from data.file_manager import read_json, write_json
from users.user_service import get_all_users

# Constants
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def save_temp_file(file):
    ensure_upload_dir()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add UUID to prevent collisions
        temp_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(filepath)
        return filepath, temp_filename
    return None, None

def parse_file_headers(filepath):
    try:
        ext = filepath.split('.')[-1].lower()
        if ext == 'csv' or ext == 'txt':
            # Try sniffing delimiter for TXT/CSV
            df = pd.read_csv(filepath, nrows=5)
        elif ext == 'xlsx':
            df = pd.read_excel(filepath, nrows=5, engine='openpyxl')
        elif ext == 'xls':
            df = pd.read_excel(filepath, nrows=5, engine='xlrd')
        else:
            return None, "Unsupported file format"
        
        return list(df.columns), None
    except Exception as e:
        return None, str(e)

def parse_full_file(filepath, mapping):
    """
    Parses the file using the provided mapping.
    Mapping format: { 'student_id': 'Column A', 'meal_type': 'Column B', ... }
    """
    try:
        ext = filepath.split('.')[-1].lower()
        if ext == 'csv' or ext == 'txt':
            df = pd.read_csv(filepath)
        elif ext == 'xlsx':
            df = pd.read_excel(filepath, engine='openpyxl')
        elif ext == 'xls':
            df = pd.read_excel(filepath, engine='xlrd')
        else:
            return None, "Unsupported file format"

        # Apply mapping
        records = []
        for index, row in df.iterrows():
            record = {}
            for target_field, source_col in mapping.items():
                if source_col and source_col != 'Select Column' and source_col in df.columns:
                     record[target_field] = str(row[source_col]).strip()
            
            # Add metadata logic if configured (e.g. constant values from frontend config)
            # For now, we rely on mapped columns
            records.append(record)
            
        return records, None
    except Exception as e:
        return None, str(e)

def validate_records(records, configs):
    """
    Validates records against system users and rules.
    configs contains: overwrite, default_meal_type, etc.
    """
    valid_records = []
    invalid_records = []
    
    users = get_all_users()
    # Create lookup map for faster checking
    user_map = {u['id']: u for u in users}
    
    for i, record in enumerate(records):
        row_num = i + 1
        errors = []
        
        # 1. Validate Student ID
        f_id = record.get('student_id')
        if not f_id:
            errors.append("Missing Student ID")
        elif f_id not in user_map:
            errors.append(f"Student ID {f_id} not found in system")
        else:
            record['user_name'] = user_map[f_id]['name'] # Enrich data
            
        # 2. Validate Meal Type (if mapped)
        if 'meal_type' in record:
             meal = record['meal_type'].lower()
             if meal not in ['breakfast', 'lunch', 'supper', 'full day', 'full_day']:
                 errors.append(f"Invalid meal type: {record['meal_type']}")
        
        # 3. Validate Status (if mapped)
        if 'status' in record:
            st = record['status'].lower()
            if st not in ['paid', 'unpaid', 'pending']:
                 errors.append(f"Invalid status: {record['status']}")

        # 4. Normalize Method (if mapped)
        if 'method' in record:
            m = str(record['method']).lower()
            if 'money' in m or 'mm' in m or 'mtn' in m or 'airtel' in m:
                record['method'] = 'Mobile Money'
            elif 'bank' in m or 'transfer' in m or 'eft' in m:
                record['method'] = 'Bank'
            else:
                record['method'] = record['method'] # Keep as is otherwise

        if errors:
            record['errors'] = "; ".join(errors)
            record['valid'] = False
            record['row'] = row_num
            invalid_records.append(record)
        else:
            record['valid'] = True
            record['row'] = row_num
            # Apply defaults if missing
            if 'status' not in record: record['status'] = 'Paid'
            
            valid_records.append(record)
            
    return valid_records, invalid_records

def apply_confirmed_payments(valid_records, configs):
    """
    Updates the system payments.xlsx/DB with valid records.
    """
    from payments.payment_service import create_payment
    
    count = 0
    # Current timestamp for all
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for record in valid_records:
        # Construct payment object expected by payment_service
        payment_data = {
            "student_id": record['student_id'],
            "student_name": record.get('user_name', 'Unknown'),
            "amount": record.get('amount', 0),
            "date": ts, 
            "meal_type": record.get('meal_type', configs.get('default_meal_type', 'Full Day')),
            "status": record.get('status', 'Paid'),
            "semester": configs.get('semester', 'Current'),
            "method": record.get('method', 'Finance Upload')
        }
        
        # We could add logic here to check overwrite, but create_payment usually appends
        # To support overwrite, we'd need a more complex update_or_create in payment_service
        create_payment(payment_data)
        count += 1
        
    return count
