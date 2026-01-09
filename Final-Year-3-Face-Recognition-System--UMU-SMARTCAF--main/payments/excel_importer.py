import csv
import io

def import_payments_from_file(file_storage):
    """
    Parses a CSV file and returns a list of payment records.
    For now, we'll support CSV. Excel requires openpyxl/pandas which might not be installed.
    """
    try:
        stream = io.StringIO(file_storage.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        payments = []
        for row in csv_input:
            # Expected columns: user_id, user_name, amount, status, method, description
            # We'll sanitize and prepare data
            payment_data = {
                "user_id": row.get("user_id", ""),
                "user_name": row.get("user_name", "Unknown"),
                "amount": row.get("amount", 0),
                "status": row.get("status", "Unpaid"),
                "method": row.get("method", "-"),
                "description": row.get("description", "Bulk Import")
            }
            payments.append(payment_data)
            
        return True, payments
    except Exception as e:
        return False, str(e)
