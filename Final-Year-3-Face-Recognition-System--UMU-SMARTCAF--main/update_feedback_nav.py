import os

# Base directory of the project
base_dir = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project"

# Find all relevant HTML files
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

feedback_nav = """                <li id="nav-feedback">
                    <a href="contact-support.html" class="nav__link">
                        <i class="ri-message-3-fill nav__icon"></i>
                        <span>Feedback & Complaints</span>
                    </a>
                </li>
                <li id="nav-feedback-list" style="display: none;">
                    <a href="feedback-list.html" class="nav__link">
                        <i class="ri-feedback-fill nav__icon"></i>
                        <span>Student Feedback</span>
                    </a>
                </li>"""

# Target for insertion: right before </ul> or before settings
insertion_point = '<li id="nav-settings">'

for filename in html_files:
    if filename == "feedback-list.html": continue
    
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'id="nav-feedback"' in content:
            print(f"Skipping {filename} (already has feedback link)")
            continue
            
        if insertion_point in content:
            new_content = content.replace(insertion_point, feedback_nav + "\n" + insertion_point)
            
            # Also update applyRoleBasedUI logic if it exists
            if "applyRoleBasedUI" in new_content:
                # Update student hidden list
                new_content = new_content.replace(
                    "'nav-settings', 'nav-training']",
                    "'nav-settings', 'nav-training', 'nav-feedback-list']"
                )
                
                # Update admin visibility logic
                admin_logic = """                    } else {
                        if (sidebar) sidebar.classList.add('sidebar--compact');
                        
                        const navFeedbackList = document.getElementById('nav-feedback-list');
                        const navFeedback = document.getElementById('nav-feedback');
                        if (navFeedbackList) navFeedbackList.style.display = 'block';
                        if (navFeedback) navFeedback.style.display = 'none';"""
                
                old_admin_logic = """                    } else {
                        if (sidebar) sidebar.classList.add('sidebar--compact');"""
                
                if old_admin_logic in new_content and admin_logic not in new_content:
                    new_content = new_content.replace(old_admin_logic, admin_logic)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Could not find insertion point in {filename}")
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Global sidebar update complete.")
