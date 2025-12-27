import os
import re

def standardize_sidebars(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # Ensure sidebar footer exists and has Logout
            footer_pattern = re.compile(r'<div class="sidebar__footer">.*?</div>', re.DOTALL)
            
            standard_footer = '''<div class="sidebar__footer">
                <a href="training-auth.html" id="nav-training" class="nav__link">
                    <i class="ri-brain-fill nav__icon"></i>
                    <span>Restricted Access</span>
                </a>
                <a href="logout-confirmation.html" id="nav-logout" class="nav__link">
                    <i class="ri-logout-box-line nav__icon"></i>
                    <span>Logout</span>
                </a>
            </div>'''

            if '<aside class="sidebar">' in content:
                if not footer_pattern.search(content):
                    # Add footer if missing before the closing sidebar tag
                    if '</aside>' in content:
                        content = content.replace('</aside>', standard_footer + '\n        </aside>')
                        modified = True
                else:
                    # Replace existing footer with standard one to ensure ID and content consistency
                    content = footer_pattern.sub(standard_footer, content)
                    modified = True

            # Ensure Logout is also present in nav__list (optional, but good for mobile horizontal nav)
            # However, the user said it was missing on some pages, so we already fixed sidebar footer above.
            
            # Ensure mobile CSS shows the footer
            mobile_css_hide = ".sidebar__footer {\n                display: none !important;\n            }"
            mobile_css_show = ".sidebar__footer {\n                display: flex !important;\n                flex-direction: row !important;\n                justify-content: center !important;\n                column-gap: 1.5rem !important;\n                padding-top: 0.5rem !important;\n                border-top: 1px solid hsla(0, 0%, 100%, 0.1) !important;\n            }"
            
            if mobile_css_hide in content:
                content = content.replace(mobile_css_hide, mobile_css_show)
                modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Standardized sidebar in {filename}")

if __name__ == "__main__":
    standardize_sidebars(r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project")
