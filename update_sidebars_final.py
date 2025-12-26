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
    # We want to update all files to have consistent sidebar structure
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # If it doesn't have the feedback links, try to inject them
        if 'id="nav-feedback"' not in content and insertion_point in content:
            content = content.replace(insertion_point, feedback_nav + "\n" + insertion_point)
            print(f"Injected feedback links into {filename}")
        
        # Now update applyRoleBasedUI logic to handle the new links
        if "applyRoleBasedUI" in content:
            # 1. Update student hidden list if 'nav-feedback-list' is missing from it
            if "'nav-feedback-list'" not in content:
                # Try to find a common hidden list pattern
                content = content.replace(
                    "'nav-settings', 'nav-training']",
                    "'nav-settings', 'nav-training', 'nav-feedback-list']"
                )
            
            # 2. Update admin/staff logic to show nav-feedback-list and hide nav-feedback
            admin_logic_injected = """                        const navFeedbackList = document.getElementById('nav-feedback-list');
                        const navFeedback = document.getElementById('nav-feedback');
                        if (navFeedbackList) navFeedbackList.style.display = 'block';
                        if (navFeedback) navFeedback.style.display = 'none';"""
            
            if admin_logic_injected not in content:
                # Find the 'else' block for admins/staff
                staff_pattern = "if (sidebar) sidebar.classList.add('sidebar--compact');"
                if staff_pattern in content:
                    content = content.replace(staff_pattern, staff_pattern + "\n\n" + admin_logic_injected)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Global sidebar and role-logic update complete.")
