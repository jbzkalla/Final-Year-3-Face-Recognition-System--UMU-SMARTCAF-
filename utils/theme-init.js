/**
 * UMU SmartCaf Theme Manager
 * 
 * This script ensures the system theme (light/dark) is applied consistently across all pages.
 * It is meant to be included at the top of every HTML file for rapid theme application.
 */

(function () {
    // 1. Check local storage first for instant application
    const cachedTheme = localStorage.getItem('umu_smart_caf_theme');
    if (cachedTheme) {
        document.documentElement.setAttribute('data-theme', cachedTheme);
    }


    // 2. Fetch official setting from backend to sync (optional but good for consistency)
    async function syncTheme() {
        try {
            const response = await fetch('/api/admin/settings');
            const settings = await response.json();

            if (settings && settings.theme) {
                const theme = settings.theme;
                document.documentElement.setAttribute('data-theme', theme);
                localStorage.setItem('umu_smart_caf_theme', theme);

                // If on settings page, sync the select dropdown
                const themeSelect = document.getElementById('theme');
                if (themeSelect) {
                    themeSelect.value = theme;
                }
            }
        } catch (error) {
            console.error('Theme synchronization failed:', error);
        }
    }

    // 3. User Role Based Visibility
    async function syncUserVisibility() {
        try {
            const response = await fetch('/api/session');
            const data = await response.json();

            if (data.success && data.user) {
                const role = data.user.role.toLowerCase();
                if (role === 'student') {
                    // Hide admin-only sidebar links
                    const adminNavItems = [
                        'nav-users', 'nav-attendance', 'nav-finance',
                        'nav-reports', 'nav-settings', 'nav-training', 'nav-menu-mgmt'
                    ];
                    adminNavItems.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) {
                            // If it's a list item parent, hide that, otherwise hide the element
                            if (el.tagName === 'LI') el.style.display = 'none';
                            else if (el.parentElement.tagName === 'LI') el.parentElement.style.display = 'none';
                            else el.style.display = 'none';
                        }
                    });

                    // Hide specialized buttons/sections
                    const adminActions = [
                        'btn-start-attendance', 'btn-add-user', 'btn-train-model'
                    ];
                    adminActions.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) el.style.display = 'none';
                    });


                }
            }

        } catch (error) {
            console.error('Session visibility sync failed:', error);
        }
    }

    // Wait for DOM to be ready for sync to avoid blocking initial render
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
