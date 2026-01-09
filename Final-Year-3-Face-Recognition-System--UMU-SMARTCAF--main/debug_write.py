from utils.constants import USERS_DB_FILE
from data.file_manager import write_json, read_json
import os
import sys

print(f"Path: {USERS_DB_FILE}", flush=True)

if not os.path.exists(os.path.dirname(USERS_DB_FILE)):
    print(f"Dir does not exist: {os.path.dirname(USERS_DB_FILE)}", flush=True)

try:
    data = read_json(USERS_DB_FILE)
    print(f"Read {len(data)} users.", flush=True)
except Exception as e:
    print(f"Read failed: {e}", flush=True)
    data = []

# Don't actually append garbage, just rewrite what we read to test permissions
# data.append({"test": "write"}) 
success = write_json(USERS_DB_FILE, data)
print(f"Write success: {success}", flush=True)
