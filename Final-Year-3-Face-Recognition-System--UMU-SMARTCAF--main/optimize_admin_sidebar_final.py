import os

base_dir = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project"
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

# Highly aggressive compact styling
aggressive_css = """
        /* Final Compact Sidebar - Zero Scroll for Admin */
        .sidebar--compact { padding: 0.5rem 0.75rem !important; }
        .sidebar--compact .sidebar__logo { margin-bottom: 0.4rem !important; }
        .sidebar--compact .sidebar__logo-img { width: 30px !important; height: 30px !important; }
        .sidebar--compact .sidebar__logo-text { font-size: 1rem !important; }
        .sidebar--compact .nav__list { row-gap: 0.1rem !important; }
        .sidebar--compact .nav__link { padding: 0.35rem 0.7rem !important; font-size: 0.85rem !important; }
        .sidebar--compact .sidebar__footer { margin-top: auto !important; padding-top: 0.3rem !important; }
        .sidebar--compact .nav__icon { font-size: 1.1rem !important; min-width: 20px !important; }
"""

for filename in html_files:
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "sidebar--compact" in content:
            # Inject at the very end of style tag to ensure override
            if "</style>" in content:
                # Remove any previously injected compact CSS if we can identify it, 
                # or just append this one which will override due to !important and position
                content = content.replace("</style>", aggressive_css + "\n    </style>")
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Applied aggressive compact styles to {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")

print("Global aggressive optimization complete.")
