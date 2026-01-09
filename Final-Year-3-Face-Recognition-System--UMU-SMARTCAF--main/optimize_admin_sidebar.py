import os

# Base directory of the project
base_dir = r"c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project"

# Find all relevant HTML files
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

compact_css = """
        /* Compact Sidebar for Admin/Staff to prevent scrolling */
        .sidebar--compact .nav__list {
            row-gap: 0.2rem !important;
        }

        .sidebar--compact .nav__link {
            padding: 0.5rem 0.8rem !important;
            font-size: 0.9rem !important;
        }

        .sidebar--compact .sidebar__logo {
            margin-bottom: 0.75rem !important;
        }

        .sidebar--compact .sidebar__logo-img {
            width: 35px !important;
            height: 35px !important;
        }

        .sidebar--compact .sidebar__logo-text {
            font-size: 1.1rem !important;
        }
"""

for filename in html_files:
    path = os.path.join(base_dir, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already injected
        if "sidebar--compact" in content and ".sidebar--compact" not in content:
            # We have the JS class toggling but not the CSS definition
            # Find a good place to inject CSS - usually before </style>
            if "</style>" in content:
                content = content.replace("</style>", compact_css + "\n    </style>")
                print(f"Injected compact CSS into {filename}")
            
            # Ensure the sidebar footer is also tucked in
            if ".sidebar__footer {" in content and "margin-top: auto" not in content:
                 content = content.replace(".sidebar__footer {", ".sidebar__footer {\n            margin-top: auto !important;")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Global sidebar optimization complete.")
