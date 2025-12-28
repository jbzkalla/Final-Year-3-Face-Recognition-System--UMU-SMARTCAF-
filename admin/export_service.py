import json
import csv
import os
import io
import zipfile
import pandas as pd
from flask import send_file
from utils.constants import DATA_DIR, BASE_DIR

FINANCE_FILE = os.path.join(BASE_DIR, 'UMU_SmartCaf_Finance_Upload_Final.csv')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.csv')

def export_all_data(export_format):
    """
    Exports all system data (Users, Attendance, Finance) in the requested format.
    """
    try:
        # Load data
        # Users
        users_data = []
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
        
        # Attendance
        attendance_data = []
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                attendance_data = list(reader)
        
        # Finance
        finance_data = []
        if os.path.exists(FINANCE_FILE):
            with open(FINANCE_FILE, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                finance_data = list(reader)

        if export_format == 'json':
            all_data = {
                "users": users_data,
                "attendance": attendance_data,
                "finance": finance_data
            }
            return json.dumps(all_data, indent=4).encode('utf-8'), "application/json", "export.json"

        elif export_format == 'csv':
            # Since CSV is a flat format, we concatenate them with headers or just zip multiple CSVs
            # But the user asked for "any format" and expected a single file usually.
            # I'll create a single large CSV with sections or just ZIP them if CSV is selected.
            # Actually, a single CSV with multiple datasets is messy. 
            # Let's provide a ZIP containing 3 CSVs if format is 'csv'.
            return create_zip_export(users_data, attendance_data, finance_data, "csv")

        elif export_format == 'xlsx':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                if users_data:
                    pd.DataFrame(users_data).to_excel(writer, sheet_name='Users', index=False)
                if attendance_data:
                    pd.DataFrame(attendance_data).to_excel(writer, sheet_name='Attendance', index=False)
                if finance_data:
                    pd.DataFrame(finance_data).to_excel(writer, sheet_name='Finance', index=False)
            output.seek(0)
            return output.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "export.xlsx"

        elif export_format == 'zip':
            return create_zip_export(users_data, attendance_data, finance_data, "original")

        else:
            return None, None, None

    except Exception as e:
        print(f"Export error: {e}")
        return None, None, None

def create_zip_export(users, attendance, finance, mode="csv"):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        if mode == "csv" or mode == "original":
            # Users to JSON or CSV
            if users:
                if mode == "csv":
                    zf.writestr("users.csv", dicts_to_csv(users))
                else:
                    zf.writestr("users.json", json.dumps(users, indent=4))
            
            # Attendance
            if attendance:
                zf.writestr("attendance.csv", dicts_to_csv(attendance))
            
            # Finance
            if finance:
                zf.writestr("finance.csv", dicts_to_csv(finance))
    
    output.seek(0)
    return output.read(), "application/zip", "export.zip"

def dicts_to_csv(dicts):
    if not dicts:
        return ""
    output = io.StringIO()
    keys = dicts[0].keys()
    writer = csv.DictWriter(output, fieldnames=keys)
    writer.writeheader()
    writer.writerows(dicts)
    return output.getvalue()
