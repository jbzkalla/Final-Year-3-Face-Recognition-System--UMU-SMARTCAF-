
import os

file_path = r'c:\Users\HP G3\Desktop\try wee3\attendance-report.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Indices from investigation:
# 311: <body> (First one)
# 509: <body> (Second one)
# We remove 311 up to 508.
# So we keep [:311] and [509:]

print(f"Index 311: {lines[311].strip()}")
print(f"Index 509: {lines[509].strip()}")

if '<body>' in lines[311] and '<body>' in lines[509]:
    new_lines = lines[:311] + lines[509:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("".join(new_lines))
    print("File fixed successfully (Indices 311/509).")
else:
    print("Verification failed.")
