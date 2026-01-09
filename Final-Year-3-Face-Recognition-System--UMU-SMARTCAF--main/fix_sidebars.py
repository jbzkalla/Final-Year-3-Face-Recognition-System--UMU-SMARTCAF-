import os

files_to_update = [
    "dashboard.html",
    "users-list.html",
    "attendance-control.html",
    "reports-dashboard.html",
    "system-settings.html",
    "add-user.html",
    "edit-user.html", 
    "payment-dashboard.html",
    "user-activity-report.html"
]

base_dir = r"c:\Users\HP G3\Desktop\try wee3"

finance_link = """                <li>
                    <a href="finance-upload.html" class="nav__link">
                        <i class="ri-upload-cloud-line nav__icon"></i>
                        <span>Finance Upload</span>
                    </a>
                </li>"""

attendance_str = """                        <i class="ri-calendar-check-line nav__icon"></i>
                        <span>Attendance</span>
                    </a>
                </li>"""

for filename in files_to_update:
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        print(f"Skipping {filename} (not found)")
        continue
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "finance-upload.html" in content:
            print(f"Skipping {filename} (already has link)")
            continue
            
        if attendance_str in content:
            # Insert after attendance
            new_content = content.replace(attendance_str, attendance_str + "\n" + finance_link)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Could not find insertion point in {filename}")
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")
