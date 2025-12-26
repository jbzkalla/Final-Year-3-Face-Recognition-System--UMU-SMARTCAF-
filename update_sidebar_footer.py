import os
import re

def update_sidebar_footers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the footer block
    footer_match = re.search(r'<div class="sidebar__footer">.*?</div>', content, re.DOTALL)
    if not footer_match:
        return

    footer_content = footer_match.group(0)
    
    # Check if the training link is already IN THE FOOTER
    if 'training-auth.html' in footer_content:
        print(f"Skipped {os.path.basename(file_path)} (Already in footer)")
        return

    # Pattern to insert before Logout link
    logout_pattern = r'(\s*)<a href="logout-confirmation\.html".*?</a>'
    
    train_link = r'\1<a href="training-auth.html" class="nav__link">\1    <i class="ri-brain-line nav__icon"></i>\1    <span>Restricted Access</span>\1</a>'

    # Replace within the footer content
    new_footer_content = re.sub(logout_pattern, train_link + r'\0', footer_content, flags=re.DOTALL)
    
    # Put updated footer back in content
    new_content = content.replace(footer_content, new_footer_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated sidebar footer for {os.path.basename(file_path)}")

def main():
    directory = r'c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project'
    for f in os.listdir(directory):
        if f.endswith('.html'):
            update_sidebar_footers(os.path.join(directory, f))

if __name__ == "__main__":
    main()
