import os
import re

def apply_text_visibility_theme(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(file_path)
    
    # Professional themes configuration
    premium_dark = {
        'headers': '#ffffff',  # White headers for Premium Dark
        'text': '#ffffff',     # Pure white for all normal text
        'gold': '#ffd700',
        'bg_active': '#610a0a' # Button/Active bg stays maroon for contrast
    }
    
    glass_light = {
        'headers': '#0858c7',  # Blue headers for Glass Light (Default)
        'black': '#000000',    # Black for specific details/stats/EVERY TEXT
        'text': '#610a0a',     # Maroon text (Base)
        'white': '#ffffff',
        'gold': '#ffd700',
        'bg_active': '#0858c7' # Blue active state for light theme
    }

    # Clean up any existing override blocks
    content = re.sub(r'/\* Professional Designer Theme Overrides \*/.*?/\* (End Overrides|End Overrides \*/) \*/?', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Minimal Logo Branding Override \*/.*?/\* (End Overrides|End Overrides \*/) \*/?', '', content, flags=re.DOTALL)

    live_attendance_specific = ""
    if filename == 'live-attendance.html':
        live_attendance_specific = f"""
        /* SPECIAL EXEMPTION: Live Attendance Overlay */
        :root:not([data-theme="light"]) .rec-name, :root:not([data-theme="light"]) .stat-value, :root:not([data-theme="light"]) .rec-status {{
            color: #ffffff !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8) !important;
        }}
        :root:not([data-theme="light"]) td {{ color: #ffd700 !important; font-weight: 500 !important; }}
        :root:not([data-theme="light"]) td:nth-child(2) {{ color: #ffffff !important; font-weight: 700 !important; }}
        """

    override_css = f"""
        /* Professional Designer Theme Overrides */
        
        /* =========================================
           0. GLOBAL FONT STANDARDIZATION
           ========================================= */
        @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap");

        * {{
            font-family: 'Poppins', sans-serif !important;
        }}

        /* =========================================
           0.1 GLOBAL FONT SIZE STANDARDIZATION (Matching Reference)
           ========================================= */
        .header__title {{
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }}

        .clock {{
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            letter-spacing: 1px !important;
        }}

        .user-name {{
            font-size: 1rem !important;
            font-weight: 600 !important;
        }}

        .user-role {{
            font-size: 0.85rem !important;
            opacity: 0.8 !important;
        }}

        .user-avatar {{
            width: 45px !important;
            height: 45px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }}

        /* =========================================
           0.2 GLOBAL SIDEBAR COMPACTNESS (Full Visibility)
           ========================================= */
        .sidebar {{
            padding: 1rem !important;
            display: flex !important;
            flex-direction: column !important;
        }}

        .sidebar__logo {{
            margin-bottom: 1.25rem !important;
        }}

        .nav__list {{
            row-gap: 0.25rem !important;
        }}

        .nav__link {{
            padding: 0.5rem 0.75rem !important;
            column-gap: 0.75rem !important;
            font-size: 0.9rem !important;
        }}

        .sidebar__logo-img {{
            width: 35px !important;
        }}

        /* =========================================
           1. PREMIUM DARK THEME (WHITE HEADERS & KEY STATS)
           ========================================= */
        :root:not([data-theme="light"]) body, 
        :root:not([data-theme="dark"]) body, 
        :root:not([data-theme="light"]) p, 
        :root:not([data-theme="light"]) label, 
        :root:not([data-theme="light"]) .input-label, 
        :root:not([data-theme="light"]) .clock, 
        :root:not([data-theme="light"]) .detail-label, 
        :root:not([data-theme="light"]) .help-text,
        :root:not([data-theme="light"]) .meal-desc {{
            color: {premium_dark["text"]} !important;
        }}

        :root:not([data-theme="light"]) h1, 
        :root:not([data-theme="light"]) h2, 
        :root:not([data-theme="light"]) h3, 
        :root:not([data-theme="light"]) h4, 
        :root:not([data-theme="light"]) .header__title, 
        :root:not([data-theme="light"]) .section-title, 
        :root:not([data-theme="light"]) .section-header span,
        :root:not([data-theme="light"]) .card-header h2, 
        :root:not([data-theme="light"]) .card__title, 
        :root:not([data-theme="light"]) .card__value,
        :root:not([data-theme="light"]) .setting-title, 
        :root:not([data-theme="light"]) .auth-title, 
        :root:not([data-theme="light"]) .login__title,
        :root:not([data-theme="light"]) .login__label,
        :root:not([data-theme="light"]) .login__register,
        :root:not([data-theme="light"]) .login__forgot,
        :root:not([data-theme="light"]) .sign,
        :root:not([data-theme="light"]) .detail-value,
        :root:not([data-theme="light"]) td,
        :root:not([data-theme="light"]) .user-name,
        :root:not([data-theme="light"]) .user-role,
        :root:not([data-theme="light"]) .notif-text,
        :root:not([data-theme="light"]) .notif-time,
        :root:not([data-theme="light"]) .control-label,
        :root:not([data-theme="light"]) .status-indicator,
        :root:not([data-theme="light"]) .radio-option,
        :root:not([data-theme="light"]) .meal-name,
        :root:not([data-theme="light"]) .form-label,
        :root:not([data-theme="light"]) th {{
            color: {premium_dark["headers"]} !important;
            font-weight: 600 !important;
        }}

        :root:not([data-theme="light"]) .nav__link.active, 
        :root:not([data-theme="light"]) .nav__link:hover {{
            background-color: {premium_dark["bg_active"]} !important;
            color: #ffffff !important;
        }}
        
        :root:not([data-theme="light"]) .nav__icon, 
        :root:not([data-theme="light"]) .card__icon, 
        :root:not([data-theme="light"]) .clock, 
        :root:not([data-theme="light"]) .sidebar__logo-text,
        :root:not([data-theme="light"]) .ri-checkbox-circle-line,
        :root:not([data-theme="light"]) .ri-eye-line,
        :root:not([data-theme="light"]) .header__subtitle,
        :root:not([data-theme="light"]) .file-upload-area p,
        :root:not([data-theme="light"]) .section-header a,
        :root:not([data-theme="light"]) .meal-time,
        :root:not([data-theme="light"]) i {{
            color: {premium_dark["gold"]} !important;
        }}

        :root:not([data-theme="light"]) .vote-bar {{
            display: none !important;
        }}

        /* =========================================
           2. GLASS LIGHT THEME (TOTAL BLACK TEXT & BLUE ACCENTS)
           ========================================= */
        [data-theme="light"] body, 
        [data-theme="light"] p, 
        [data-theme="light"] .clock, 
        [data-theme="light"] .notif-text, 
        [data-theme="light"] .notif-time,
        [data-theme="light"] .meal-desc {{
            color: {glass_light["black"]} !important;
        }}

        /* EXHAUSTIVE BLACK TEXT RULE FOR ALL LABELS & HEADERS IN GLASS THEME */
        [data-theme="light"] h1, 
        [data-theme="light"] h2, 
        [data-theme="light"] h3, 
        [data-theme="light"] h4, 
        [data-theme="light"] .section-title, 
        [data-theme="light"] .section-header span,
        [data-theme="light"] .card-header h2, 
        [data-theme="light"] .card__title, 
        [data-theme="light"] .card__value,
        [data-theme="light"] .setting-title, 
        [data-theme="light"] .auth-title, 
        [data-theme="light"] .login__title,
        [data-theme="light"] .form-label,
        [data-theme="light"] label,
        [data-theme="light"] .input-label,
        [data-theme="light"] .detail-label,
        [data-theme="light"] .detail-value,
        [data-theme="light"] .help-text,
        [data-theme="light"] .login__label,
        [data-theme="light"] th,
        [data-theme="light"] td,
        [data-theme="light"] .user-name,
        [data-theme="light"] .user-role,
        [data-theme="light"] .stat-value,
        [data-theme="light"] .total-count,
        [data-theme="light"] .value-text,
        [data-theme="light"] .summary-value,
        [data-theme="light"] .rec-name,
        [data-theme="light"] .rec-status,
        [data-theme="light"] .status-indicator,
        [data-theme="light"] .meal-name,
        [data-theme="light"] .sign,
        [data-theme="light"] .login__register,
        [data-theme="light"] .login__forgot,
        [data-theme="light"] .report-analytics,
        [data-theme="light"] .popularity-stat,
        [data-theme="light"] .chart-label,
        [data-theme="light"] .feedback-text,
        [data-theme="light"] .complaint-detail,
        [data-theme="light"] .feedback-content,
        [data-theme="light"] .feedback-list-item h4 {{
            color: {glass_light["black"]} !important;
        }}

        /* MENU REFINEMENTS - GLASS THEME */
        [data-theme="light"] .meal-category {{
            color: #821005 !important;
            font-weight: 600 !important;
        }}

        [data-theme="light"] .vote-btn span {{
            color: #821005 !important;
            font-weight: 600 !important;
        }}

        [data-theme="light"] .vote-bar {{
            display: flex !important;
        }}

        /* SPECIFIC PAGE TITLE COLOR REFINEMENT */
        [data-theme="light"] .header__title {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        /* SIDEBAR WHITE GLASS THEME REFINEMENT */
        [data-theme="light"] .sidebar {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}

        [data-theme="light"] .sidebar__logo-text,
        [data-theme="light"] .nav__link,
        [data-theme="light"] .sidebar__footer .nav__link span,
        [data-theme="light"] .nav__link span {{
            color: #000000 !important;
            font-weight: 500 !important;
        }}

        [data-theme="light"] .nav__link.active, 
        [data-theme="light"] .nav__link:hover {{
            background-color: {glass_light["bg_active"]} !important;
            color: #ffffff !important;
        }}
        
        [data-theme="light"] .nav__icon, 
        [data-theme="light"] .card__icon, 
        [data-theme="light"] .clock, 
        [data-theme="light"] .sidebar__logo-text,
        [data-theme="light"] .ri-checkbox-circle-line,
        [data-theme="light"] i {{
            color: {glass_light["gold"]} !important;
        }}

        .clock {{
            font-weight: 600 !important;
            letter-spacing: 1px !important;
        }}

        /* Standardize Background Consistency for all pages */
        .dashboard__img, .login__img, .register__img, .auth__img {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            object-fit: cover !important;
            object-position: center !important;
            z-index: -1 !important;
            pointer-events: none !important;
        }}

        /* Common Button Styles Across Themes (Applying Designer Maroon/Gold) */
        :root .btn-primary, :root .btn-action, :root .btn-add, :root .btn-start, :root .login__button {{
            background-color: #610a0a !important;
            border: 2px solid #ffd700 !important;
            color: #ffd700 !important;
        }}

        /* WHITE TEXT FOR SPECIFIC ACTION BUTTONS (Visibility on Glass/Premium) */
        [data-theme="light"] .btn-back,
        [data-theme="light"] .btn-cancel,
        [data-theme="light"] .btn-secondary,
        [data-theme="light"] .btn-stay-logged-in,
        [data-theme="light"] .btn-go-back,
        [data-theme="light"] .btn-discharge,
        [data-theme="light"] .btn-danger,
        [data-theme="light"] .btn-close,
        [data-theme="light"] .btn-discard,
        [data-theme="light"] .modal-overlay a,
        [data-theme="light"] .modal-overlay button,
        [data-theme="light"] .btn-logout {{
            color: {glass_light["white"]} !important;
        }}

        /* HEADER GLASS EFFECT REFINEMENT (Matching Reference Photo) */
        [data-theme="light"] .header {{
            background-color: rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            border-radius: 1.25rem !important;
        }}

        [data-theme="light"] .header__subtitle {{
            color: #222222 !important;
            font-weight: 500 !important;
            opacity: 0.9 !important;
        }}

        [data-theme="light"] .user-avatar {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid rgba(0, 0, 0, 0.1) !important;
        }}

        /* MODAL GLASS THEME REFINEMENT */
        [data-theme="light"] .modal-content {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.2) !important;
            color: #000000 !important;
        }}

        [data-theme="light"] .modal-content *, 
        [data-theme="light"] .modal-body strong,
        [data-theme="light"] .status-select {{
            color: #000000 !important;
        }}

        [data-theme="light"] .modal-close {{
            color: #000000 !important;
        }}

        [data-theme="light"] .status-select {{
            background: rgba(0, 0, 0, 0.05) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}

        {live_attendance_specific}
        /* End Overrides */
    """

    if '</style>' in content:
        content = content.replace('</style>', override_css + '\n    </style>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    directory = r'c:\Users\HP G3\Desktop\Bwanika Joseph Final Year3 Project\Bwanika Joseph Final UMU SmartCaf Project\Bwanika Joseph Final UMU SmartCaf Project'
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    for f in html_files:
        apply_text_visibility_theme(os.path.join(directory, f))
    print(f"Theme Updated: Applied Exhaustive Glass Theme refinements to {len(html_files)} files.")

if __name__ == "__main__":
    main()
