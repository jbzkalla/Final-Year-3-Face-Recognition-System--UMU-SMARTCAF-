import os

base_dir = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project"
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

compact_css = """
        /* Compact Sidebar for Admin/Staff */
        .sidebar--compact .nav__list { row-gap: 0.15rem !important; }
        .sidebar--compact .nav__link { padding: 0.45rem 0.8rem !important; font-size: 0.88rem !important; }
        .sidebar--compact .sidebar__logo { margin-bottom: 0.5rem !important; }
        .sidebar--compact .sidebar__logo-img { width: 32px !important; height: 32px !important; }
        .sidebar--compact .sidebar__logo-text { font-size: 1.05rem !important; }
        .sidebar--compact .sidebar__footer { margin-top: auto !important; padding-top: 0.5rem !important; }
"""

updated_count = 0
for filename in html_files:
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # If it has the role-based logic or is a known admin page, ensure CSS is there
        has_logic = "sidebar--compact" in content
        missing_css = ".sidebar--compact" not in content
        
        if has_logic:
            if missing_css:
                if "</style>" in content:
                    content = content.replace("</style>", compact_css + "\n    </style>")
                    updated_count += 1
                    print(f"Added CSS to {filename}")
                else:
                    print(f"Missing style tag in {filename}")
            else:
                # Update existing compact CSS if it looks old
                if "row-gap: 0.2rem" in content or "padding: 0.5rem" in content:
                    # We can replace the old block if it matches our previous script's output
                    pass 
                print(f"Skipping {filename} - CSS already exists")

            # Final check to ensure row-gap is very small
            content = content.replace("row-gap: 0.4rem !important;", "row-gap: 0.25rem !important;")
            content = content.replace("padding: 0.65rem 1rem !important;", "padding: 0.55rem 0.9rem !important;")

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error {filename}: {e}")

print(f"Summary: Updated {updated_count} files.")
