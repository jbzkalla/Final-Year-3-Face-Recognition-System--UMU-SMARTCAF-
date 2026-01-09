import json
import os
import random

# Path to the payments database
DATA_DIR = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project\data"
PAYMENTS_FILE = os.path.join(DATA_DIR, "payments.json")

def diversify_data():
    if not os.path.exists(PAYMENTS_FILE):
        print(f"File not found: {PAYMENTS_FILE}")
        return

    with open(PAYMENTS_FILE, 'r') as f:
        payments = json.load(f)

    updated_count = 0
    methods = ["Bank", "Mobile Money"]
    
    for p in payments:
        # Only diversify those that were previously "Legacy Import" or "Manual Entry" 
        # or anything other than the new standards, but specifically for PAID status
        if p.get('status') == 'Paid' and p.get('method') not in ["Bank", "Mobile Money"]:
            p['method'] = random.choice(methods)
            updated_count += 1

    with open(PAYMENTS_FILE, 'w') as f:
        json.dump(payments, f, indent=4)

    print(f"Successfully updated {updated_count} payment records with realistic methods.")

if __name__ == "__main__":
    diversify_data()
