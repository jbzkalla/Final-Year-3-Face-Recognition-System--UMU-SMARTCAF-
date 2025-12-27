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

    // Add CSS to handle instant hiding based on role classes
    const style = document.createElement('style');
    style.innerHTML = `
        /* Hide admin elements instantly if role is student */
        .role-student .admin-only,
        .role-student #nav-users, .role-student #nav-attendance, 
        .role-student #nav-finance, .role-student #nav-reports, 
        .role-student #nav-settings, .role-student #nav-training, 
        .role-student #nav-menu-mgmt, .role-student #nav-feedback-list {
            display: none !important;
        }

        /* Show student elements if role is student */
        .role-student .student-only, .role-student #nav-feedback {
            display: flex !important;
        }

        /* Staff Role Specifics */
        .role-staff #nav-settings { display: none !important; }
        .role-staff #nav-feedback-list { display: block !important; }
        .role-staff #nav-feedback { display: none !important; }

        /* Admin Role Specifics */
        .role-admin #nav-feedback-list { display: block !important; }
        .role-admin #nav-feedback { display: none !important; }
        
        /* Ensure Logout is ALWAYS visible */
        .nav-logout, #nav-logout, .sidebar__footer {
            display: flex !important;
        }
    `;
    document.head.appendChild(style);


    async function syncTheme() {
        try {
            const response = await fetch('/api/admin/settings');
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
        });
    } else {
        syncTheme();
        syncUserVisibility();
    }
})();
