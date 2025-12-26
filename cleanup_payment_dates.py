import json
import os
from datetime import datetime

PAYMENTS_JSON = 'data/payments.json'

def cleanup_dates():
    if not os.path.exists(PAYMENTS_JSON):
        return
        
    with open(PAYMENTS_JSON, 'r', encoding='utf-8') as f:
        payments = json.load(f)
        
    for p in payments:
        date_str = p.get('date')
        if not date_str:
            continue
            
        # Try to parse M/D/YYYY and convert to YYYY-MM-DD
        if '/' in date_str:
            try:
                dt = datetime.strptime(date_str, "%m/%d/%Y")
                p['date'] = dt.strftime("%Y-%m-%d")
            except:
                try:
                    # Maybe it's D/M/YYYY
                    dt = datetime.strptime(date_str, "%d/%m/%Y")
                    p['date'] = dt.strftime("%Y-%m-%d")
                except:
                    pass
                    
    with open(PAYMENTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(payments, f, indent=4)
    
    print("✓ Sanitized payment dates in JSON database")

if __name__ == "__main__":
    cleanup_dates()
