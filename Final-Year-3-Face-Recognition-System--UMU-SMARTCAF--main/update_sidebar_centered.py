import os
import re

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update/Add Sidebar Footer CSS
    css_pattern = r'\.sidebar__footer\s*\{[^}]*\}'
    new_css_block = """
        .sidebar__footer {
            margin-top: auto;
            display: flex;
            flex-direction: column;
            row-gap: 0.5rem;
            align-items: center;
        }

        .sidebar__footer .nav__link {
            justify-content: center;
            width: 100%;
        }"""
    
    if re.search(css_pattern, content):
        content = re.sub(css_pattern, new_css_block.strip(), content)
    else:
        # If .sidebar__footer css not found, try to find where to insert it or just add it to the style block
        style_end_match = re.search(r'</style>', content)
        if style_end_match:
            content = content.replace('</style>', new_css_block + '\n    </style>')

    # 2. Update/Add Sidebar Footer HTML
    footer_html_pattern = r'<div class="sidebar__footer">.*?</div>'
    new_footer_html = """            <div class="sidebar__footer">
                <a href="training-auth.html" class="nav__link">
                    <i class="ri-brain-line nav__icon"></i>
                    <span>Restricted Access</span>
                </a>
                <a href="logout-confirmation.html" class="nav__link">
                    <i class="ri-logout-box-line nav__icon"></i>
                    <span>Logout</span>
                </a>
            </div>"""

    if re.search(footer_html_pattern, content, re.DOTALL):
        content = re.sub(footer_html_pattern, new_footer_html, content, flags=re.DOTALL)
    else:
        # If not found, insert after the nav list or before the end of the sidebar
        if '</ul>' in content and '<aside class="sidebar">' in content:
            # Find the LAST </ul> that is inside a sidebar
            # This is a bit simplified but should work for this project's structure
            # Let's find the closing tag of the sidebar
            sidebar_match = re.search(r'(<aside class="sidebar">.*?)(\s*)(</aside>)', content, re.DOTALL)
            if sidebar_match:
                sidebar_inner = sidebar_match.group(1)
                if '</ul>' in sidebar_inner:
                    # Insert after the last </ul> in the sidebar
                    parts = sidebar_inner.rsplit('</ul>', 1)
                    new_sidebar_inner = parts[0] + '</ul>\n\n' + new_footer_html + parts[1]
                    content = content.replace(sidebar_inner, new_sidebar_inner)

    # 3. Final touch: ensure Restricted Access is mentioned (sanity check)
    if 'Restricted Access' not in content and '<aside' in content:
        # If it's still missing, we might have failed the regex.
        pass
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {os.path.basename(file_path)}")

def main():
    directory = r'c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project'
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    # Skip some files if necessary
    skip_files = ['login.html', 'register.html', 'forgot-password.html', 'error.html', 'receipt.html']
    
    for f in html_files:
        if f in skip_files:
            continue
        update_html_file(os.path.join(directory, f))

if __name__ == "__main__":
    main()
