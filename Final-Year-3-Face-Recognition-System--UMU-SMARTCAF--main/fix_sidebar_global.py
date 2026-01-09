import os
import re

def fix_sidebar_css_and_visibility(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # 1. Fix Sidebar CSS: Ensure overflow-y: auto and flex layout
            if '.sidebar {' in content:
                # Add overflow-y: auto if missing
                if 'overflow-y: auto' not in content and '.sidebar' in content:
                    # Find the .sidebar { block and add overflow
                    content = content.replace('.sidebar {', '.sidebar {\n            overflow-y: auto !important;\n            display: flex !important;\n            flex-direction: column !important;')
                    modified = True

            # 2. Fix Sidebar Footer CSS: Ensure margin-top: auto
            if '.sidebar__footer {' not in content and '<div class="sidebar__footer">' in content:
                # Inject a standard style if missing
                style_tag = '<style>'
                standard_footer_css = '''
        .sidebar__footer {
            margin-top: auto !important;
            display: flex !important;
            flex-direction: column !important;
            row-gap: 0.5rem !important;
            padding-top: 1rem !important;
            border-top: 1px solid hsla(0, 0%, 100%, 0.1) !important;
        }
'''
                if style_tag in content:
                    content = content.replace(style_tag, style_tag + standard_footer_css)
                    modified = True
            elif '.sidebar__footer {' in content:
                # Ensure it has margin-top: auto
                if 'margin-top: auto' not in content:
                    content = content.replace('.sidebar__footer {', '.sidebar__footer {\n            margin-top: auto !important;')
                    modified = True

            # 3. Remove inline scripts that hide nav-training for students
            # The user wants "same display look" including Restricted Access
            hiding_pattern = r"['\"]nav-training['\"],\s*"
            if re.search(hiding_pattern, content):
                content = re.sub(hiding_pattern, "", content)
                modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed CSS/Visibility in {filename}")

if __name__ == "__main__":
    fix_sidebar_css_and_visibility(r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project")
