/**
 * UMU SmartCaf Theme Manager
 * 
 * This script ensures the system theme (light/dark) is applied consistently across all pages.
 * It is meant to be included at the top of every HTML file for rapid theme application.
 */

(function () {
    // 1. Instant Theme & Role Application
    const cachedTheme = localStorage.getItem('umu_smart_caf_theme');
    const cachedRole = localStorage.getItem('umu_smart_caf_role');

    if (cachedTheme) {
        document.documentElement.setAttribute('data-theme', cachedTheme);
    }

    // Apply role class instantly to avoid flickering
    if (cachedRole) {
        document.documentElement.classList.add(`role-${cachedRole.toLowerCase()}`);
    }

    // Add CSS to handle instant hiding based on role classes and mobile enhancements
    const style = document.createElement('style');
    style.innerHTML = `
        /* Role-based Visibility */
        .role-student .admin-only,
        .role-student #nav-users, .role-student #nav-attendance, 
        .role-student #nav-finance, .role-student #nav-reports, 
        .role-student #nav-settings, .role-student #nav-menu-mgmt, 
        .role-student #nav-feedback-list {
            display: none !important;
        }

        .role-student .student-only, .role-student #nav-feedback, .role-student #nav-training {
            display: flex !important;
        }

        .role-staff #nav-settings { display: none !important; }
        .role-staff #nav-feedback-list { display: block !important; }
        .role-staff #nav-feedback { display: none !important; }

        .role-admin #nav-feedback-list { display: block !important; }
        .role-admin #nav-feedback { display: none !important; }
        
        .nav-logout, #nav-logout, .sidebar__footer {
            display: flex !important;
        }

        /* Mobile Enhancements (Transitions) */
        .header { transition: background-color 0.3s ease; }

        @media screen and (max-width: 767px) {
            /* Transform Sidebar into a Slide-out Drawer */
            :root body .sidebar {
                position: fixed !important;
                left: -100% !important;
                top: 0 !important;
                width: 280px !important;
                height: 100vh !important;
                z-index: 5000 !important;
                transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
                display: flex !important;
                flex-direction: column !important;
                background-color: hsla(210, 30%, 8%, 0.98) !important;
                backdrop-filter: blur(15px) !important;
                padding: 0.75rem !important; /* Reduced padding */
                overflow-y: auto !important;
            }

            :root body .sidebar__logo {
                margin-bottom: 0.5rem !important; /* Tightened logo margin */
                justify-content: flex-start !important;
            }

            :root body .sidebar__logo-img {
                width: 35px !important;
            }

            :root body .nav__list {
                flex-direction: column !important; /* FORCED COLUMN */
                row-gap: 0.1rem !important; /* EXTREME COMPACTNESS */
                margin-top: 0 !important;
                display: flex !important;
                overflow-x: visible !important;
                padding-bottom: 0 !important;
            }

            :root body .nav__link {
                padding: 0.45rem 0.75rem !important; /* Tightened padding */
                font-size: 0.85rem !important; /* Slightly smaller for compactness */
                column-gap: 0.75rem !important;
                min-height: unset !important; /* Allow it to shrink */
            }

            :root body .nav__icon {
                font-size: 1.1rem !important;
                min-width: 24px !important;
            }

            :root body .sidebar__footer {
                margin-top: auto !important;
                padding-top: 0.5rem !important;
                row-gap: 0.1rem !important;
                border-top: 1px solid hsla(0,0%,100%,0.05) !important;
            }

            :root body .sidebar.active {
                left: 0 !important;
            }

            /* Main Layout Adjustments */
            :root body .dashboard { flex-direction: column !important; }
            :root body .main-content { 
                padding: 1rem !important; 
                padding-top: 65px !important; /* Tightened space for the header */
                overflow-x: hidden !important;
                min-height: 100vh !important;
                flex: 1 1 auto !important;
            }

            /* Fixed Header for Branding & Menu - Single Row Optimization */
            :root body .header {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                right: 0 !important;
                z-index: 4000 !important;
                margin-bottom: 0 !important;
                padding: 0.5rem 0.75rem !important;
                display: flex !important;
                flex-direction: row !important; /* Forces one row */
                justify-content: space-between !important;
                align-items: center !important;
                width: 100% !important;
                height: 55px !important; /* Explicitly reduced height */
                border-radius: 0 !important;
                border: none !important;
                border-bottom: 1px solid hsla(0,0%,100%,0.1) !important;
                gap: 0.5rem !important;
                background-color: hsla(210, 30%, 8%, 0.95) !important;
                backdrop-filter: blur(15px) !important;
            }

            /* Target the title container div */
            :root body .header > div:first-of-type {
                display: flex !important;
                align-items: center !important;
                overflow: hidden !important;
                flex: 1 !important;
            }

            :root body .header__title { 
                font-size: 0.9rem !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                margin: 0 !important;
                color: #fff !important;
            }

            /* Hide Subtitle/Date on narrow mobile header */
            :root body .header__subtitle, 
            :root body .header .date, 
            :root body .header br,
            :root body .header p { 
                display: none !important; 
            }

            :root body .header__right { 
                column-gap: 0.5rem !important; 
                display: flex !important;
                align-items: center !important;
                flex-shrink: 0 !important;
                background: none !important;
                padding: 0 !important;
                margin: 0 !important;
                width: auto !important;
                border: none !important;
            }
            
            :root body .user-info { display: none !important; }
            :root body .clock { 
                font-size: 0.8rem !important;
                color: #ffd700 !important;
                font-weight: 600 !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            :root body .user-avatar {
                width: 32px !important;
                height: 32px !important;
                font-size: 0.8rem !important;
                margin: 0 !important;
            }

            /* Hamburger Button */
            :root body #mobile-menu-toggle {
                display: flex !important;
                align-items: center;
                justify-content: center;
                width: 36px !important;
                height: 36px !important;
                background: #610a0a !important; /* Maroon */
                border: 1px solid #ffd700 !important; /* Gold border */
                border-radius: 6px !important;
                color: #ffd700 !important; /* Gold icon */
                font-size: 1.25rem !important;
                cursor: pointer !important;
                flex-shrink: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Overlay */
            :root body .sidebar-overlay {
                position: fixed !important;
                inset: 0 !important;
                background: rgba(0,0,0,0.7) !important;
                backdrop-filter: blur(3px) !important;
                z-index: 4500 !important;
                opacity: 0 !important;
                visibility: hidden !important;
                transition: all 0.3s ease !important;
            }
            :root body .sidebar-overlay.active { opacity: 1 !important; visibility: visible !important; }

            /* Universal Grid Refinements - Premium 2x2 Pattern for Small Components (Dashboard) */
                justify-content: center !important;
            }

            /* STRICT SINGLE COLUMN for Attendance, Control, and Report Generation */
            :root body .live-grid,
            :root body .left-col,
            :root body .right-col,
            :root body .live-grid .stats-container,
            :root body .control-panel,
            :root body .radio-group,
            :root body .live-grid .action-buttons,
            :root body .gen-controls,
            :root body .user-selector,
            :root body .form-grid,
            :root body .actions-bar {
                display: flex !important;
                flex-direction: column !important; /* FORCES PURE COLUMN FORM */
                width: 100% !important;
                gap: 1rem !important;
                padding: 0 !important;
            }

            :root body .btn-search,
            :root body .btn-start,
            :root body .btn-stop,
            :root body .btn-confirm-attendance {
                width: 100% !important;
                min-height: 55px !important;
                margin: 0 !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                gap: 0.5rem !important;
                border-radius: 1rem !important;
                background: #610a0a !important; /* Premium Maroon */
                color: #fff !important;
                border: 1px solid #ffd700 !important; /* Gold trim */
                font-weight: 600 !important;
                font-size: 1rem !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            }
            :root body .actions-container:not(:has(table)) {
                width: 100% !important;
                padding: 0 !important;
                margin: 0 auto 1.5rem auto !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
            }

            /* PREMIUM HORIZONTAL SCROLL for Dashboard Quick Actions */
            :root body .actions-container:not(:has(table)) {
                width: 100% !important;
                padding: 0 0.5rem !important;
                margin: 0 auto 1.25rem auto !important;
                overflow: hidden !important;
                display: block !important;
            }

            :root body .action-buttons:not(.live-grid *) {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: flex-start !important; /* Proper scroll start */
                align-items: stretch !important;
                gap: 0.75rem !important;
                width: 100% !important;
                padding: 0.5rem 0.25rem 1rem 0.25rem !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
                scrollbar-width: none !important; /* Hide scrollbar for clean look */
            }

            :root body .action-buttons:not(.live-grid *)::-webkit-scrollbar {
                display: none !important;
            }

            :root body .action-buttons:not(.live-grid *) .btn-action {
                flex: 0 0 auto !important; /* Prevent shrinking */
                width: 100px !important; /* Fixed width for consistent scroll */
                min-height: 70px !important;
                padding: 0.5rem !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                font-size: 0.7rem !important;
                border-radius: 1rem !important;
                margin: 0 !important;
                gap: 0.25rem !important;
                background-color: var(--card-bg) !important;
                backdrop-filter: blur(5px) !important;
                border: var(--glass-border) !important;
            }

            :root body .action-buttons:not(.live-grid *) .btn-action i { 
                font-size: 1.4rem !important; 
                margin: 0 !important;
            }

                padding: 0 !important;
            }

            /* Shared Vertical Control Styling */
            :root body .control-group {
                width: 100% !important;
                display: flex !important;
                flex-direction: column !important;
                gap: 0.5rem !important;
            }

            :root body .control-select,
            :root body .control-input {
                width: 100% !important;
                min-height: 48px !important;
                padding: 0.75rem !important;
                font-size: 1rem !important;
            }

            :root body .btn-generate {
                width: 100% !important;
                min-height: 55px !important;
                margin: 0 !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                gap: 0.5rem !important;
                border-radius: 1rem !important;
                background: #610a0a !important; /* Premium Maroon */
                color: #fff !important;
                border: 1px solid #ffd700 !important; /* Gold trim */
                font-weight: 600 !important;
                font-size: 1rem !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            }

            /* Refine Radio Options for Column Readability */
            :root body .radio-group {
                gap: 0.75rem !important;
                padding: 1rem !important;
                background-color: var(--glass-bg) !important;
                border-radius: 0.75rem !important;
                align-items: flex-start !important;
            }
            
            :root body .radio-option {
                width: 100% !important;
                justify-content: flex-start !important;
                padding: 0.5rem 0 !important;
                display: flex !important;
                align-items: center !important;
                gap: 0.5rem !important;
            }

            /* Full-Width Buttons for Attendance/Control */
            :root body .btn,
            :root body .live-grid .btn-action,
            :root body .control-group {
                width: 100% !important;
                margin: 0 !important;
                min-height: 55px !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
            }

            /* Professional Cinema View for Camera */
            :root body .camera-container {
                width: 100% !important;
                height: 300px !important;
                margin: 0 auto 0.5rem !important;
                border-radius: 1.25rem !important;
                overflow: hidden !important;
                order: -1;
                background: #000 !important;
                position: relative !important;
            }

            :root body .camera-feed {
                width: 100% !important;
                height: 100% !important;
                object-fit: cover !important;
                border-radius: 1.25rem !important;
            }

            /* Universal Table & Detail Centering (Matching User Management) */
            :root body .table-container,
            :root body .actions-container:has(table), /* Dashboard Table Wrapper */
            :root body .live-table-container,
            :root body .notifications-panel,
            :root body .notifications-section,
            :root body .actions-section,
            :root body .status-grid,
            :root body .details-grid,
            :root body .settings-layout,
            :root body .settings-nav,
            :root body .settings-card,
            :root body .settings-content,
            :root body .actions-bar {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch;
                padding: 1rem !important;
                margin: 0 auto 1.5rem auto !important;
                width: 95% !important;
                max-width: 1200px !important;
                display: block !important;
                background-color: var(--card-bg) !important;
                backdrop-filter: blur(10px) !important;
                border: var(--glass-border) !important;
                border-radius: 1.25rem !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
                scrollbar-width: thin;
            }
            
            :root body .settings-nav {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: flex-start !important;
                overflow-x: auto !important;
                gap: 0.5rem !important;
                padding-bottom: 0.5rem !important;
                scrollbar-width: none;
            }

            :root body .settings-tab {
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }

            :root body table,
            :root body .history-table,
            :root body .user-table,
            :root body .live-table,
            :root body .notification-list {
                width: 100% !important;
                min-width: 600px !important; 
                margin: 0 auto !important;
                border-collapse: separate !important;
                border-spacing: 0 0.5rem !important;
            }

            :root body .recognition-overlay {
                width: 90% !important;
                left: 5% !important;
                transform: none !important;
                bottom: 10px !important;
            }
        }

        @media screen and (min-width: 768px) {
            #mobile-menu-toggle { display: none !important; }
        }
    `;
    document.head.appendChild(style);

    function injectMobileUI() {
        if (window.innerWidth >= 768) return;

        // 1. Inject Hamburger to Header
        const header = document.querySelector('.header');
        if (header && !document.getElementById('mobile-menu-toggle')) {
            const toggle = document.createElement('button');
            toggle.id = 'mobile-menu-toggle';
            toggle.innerHTML = '<i class="ri-menu-line"></i>';
            header.prepend(toggle);

            toggle.addEventListener('click', () => {
                const sidebar = document.querySelector('.sidebar');
                const overlay = document.querySelector('.sidebar-overlay');
                if (sidebar) sidebar.classList.toggle('active');
                if (overlay) overlay.classList.toggle('active');
            });
        }

        // 2. Inject Overlay
        if (!document.querySelector('.sidebar-overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);
            overlay.addEventListener('click', () => {
                const sidebar = document.querySelector('.sidebar');
                if (sidebar) sidebar.classList.remove('active');
                overlay.classList.remove('active');
            });
        }
    }

    async function syncTheme() {
        try {
            const response = await fetch('/api/public/settings');
            const settings = await response.json();
            if (settings && settings.theme) {
                document.documentElement.setAttribute('data-theme', settings.theme);
                localStorage.setItem('umu_smart_caf_theme', settings.theme);
            }
        } catch (e) { }
    }

    async function syncUserVisibility() {
        try {
            const response = await fetch('/api/session');
            const data = await response.json();

            if (data.success && data.user) {
                const role = data.user.role.toLowerCase();

                // Update Cache
                localStorage.setItem('umu_smart_caf_role', role);

                // Remove existing role classes and add current one
                document.documentElement.classList.remove('role-admin', 'role-staff', 'role-student');
                document.documentElement.classList.add(`role-${role}`);

                // Apply logic to sidebar compact mode if needed
                const sidebar = document.querySelector('.sidebar');
                if (sidebar) sidebar.classList.add('sidebar--compact');

            } else {
                // If session is lost, clear cache
                localStorage.removeItem('umu_smart_caf_role');
            }
        } catch (e) { }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            syncTheme();
            syncUserVisibility();
            injectMobileUI();
        });
    } else {
        syncTheme();
        syncUserVisibility();
        injectMobileUI();
    }

    window.addEventListener('resize', injectMobileUI);
})();
