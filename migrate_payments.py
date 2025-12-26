import json
import csv
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'UMU_SmartCaf_Finance_Upload_Final.csv')
USERS_JSON = os.path.join(BASE_DIR, 'data', 'users.json')
PAYMENTS_JSON = os.path.join(BASE_DIR, 'data', 'payments.json')

def migrate():
    # Load users for ID mapping
    with open(USERS_JSON, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # Create name-to-id map
    # We use name because the old IDs in CSV (UMU2025...) might not perfectly match the new logic (UMUSTUD...)
    name_to_id = {u['name'].strip().upper(): u['id'] for u in users}
    
    payments = []
    
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Student Name'].strip().upper()
                new_id = name_to_id.get(name)
                
                if not new_id:
                    print(f"Warning: Could not find user for {name}, skipping or using old ID.")
                    new_id = row['Student ID']

                payment = {
                    "id": f"PAY-{os.urandom(4).hex().upper()}",
                    "user_id": new_id,
                    "user_name": row['Student Name'],
                    "amount": float(row['Amount Paid'].replace(',', '') or 0),
                    "date": row['Payment Date'],
                    "meal_type": row['Meal Plan'],
                    "status": row['Status'],
                    "method": "Legacy Import",
                    "description": "Initial data migration"
                }
                payments.append(payment)
    
    with open(PAYMENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(payments, f, indent=4)
        
    print(f"Successfully migrated {len(payments)} payments to {PAYMENTS_JSON}")

if __name__ == "__main__":
    migrate()
