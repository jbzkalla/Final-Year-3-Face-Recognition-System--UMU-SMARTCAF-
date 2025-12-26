import pandas as pd
import os

# Current project directory
CWD = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project"

data = {
    'Student ID': [],
    'Student Name': [],
    'Amount Paid': [],
    'Payment Date': [],
    'Meal Plan': [],
    'Status': [],
    'Payment Method': []
}

df = pd.DataFrame(data)

# Generate Excel Template
excel_path = os.path.join(CWD, "sample_finance_template.xlsx")
df.to_excel(excel_path, index=False)
print(f"Excel Template created at {excel_path}")

# Generate CSV Template (matching the user's specific file name if needed, or just a generic one)
csv_path = os.path.join(CWD, "sample_finance_template.csv")
df.to_csv(csv_path, index=False)
print(f"CSV Template created at {csv_path}")
