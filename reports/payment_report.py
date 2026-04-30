from payments.payment_service import get_all_payments, get_payment_stats
from datetime import datetime

def generate_payment_report():
    payments = get_all_payments()
    stats = get_payment_stats()
    
    return {
        "summary": stats,
        "transactions": payments
    }

def get_revenue_trends():
    payments = get_all_payments()
    # Aggregate revenue by month
    trends = {}
    for p in payments:
        if p['status'] == 'Paid':
            try:
                date_str = p['date']
                # parse YYYY-MM-DD
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                month_key = dt.strftime("%b") # e.g., Jan
                
                amt = float(str(p['amount']).replace(',', '').strip())
                trends[month_key] = trends.get(month_key, 0) + amt
            except:
                pass
                
    # Ensure chronological order if possible, or just keys
    # For simplicity, let's just return what we found, maybe sorted by months?
    # Hard to sort using just "Jan", "Feb" without year context, but let's assume current year context or just display available
    
    # If empty (no dates parsed), return empty structure
    if not trends:
        return {"labels": [], "data": []}
        
    return {
        "labels": list(trends.keys()),
        "data": list(trends.values())
    }

def get_payment_methods_distribution():
    payments = get_all_payments()
    methods = {}
    for p in payments:
        if p['status'] == 'Paid':
            m = p.get('method', 'Unknown')
            # In CSV we defaulted to "Bank/Mobile Money", maybe we can infer something or just show that
            methods[m] = methods.get(m, 0) + 1
            
    return {
        "labels": list(methods.keys()),
        "data": list(methods.values())
    }
