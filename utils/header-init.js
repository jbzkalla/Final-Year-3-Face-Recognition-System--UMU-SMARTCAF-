/**
 * header-init.js
 * Synchronizes and initializes the header user profile and real-time clock across all pages.
 */

// 1. Real-time Clock Functionality
function updateHeaderClock() {
    const clockEl = document.getElementById('realtime-clock');
    if (!clockEl) return;

    const now = new Date();
    // Format: 5:13:53 PM (Matching the user's reference photo)
    clockEl.textContent = now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
}

// 2. Dynamic Profile Initialization
async function initializeHeaderProfile() {
    const nameEl = document.getElementById('header-user-name');
    const roleEl = document.getElementById('header-user-role');
    const avatarEl = document.getElementById('header-avatar');

    // Step A: Load from Cache for Instant Feedback
    const cachedUser = localStorage.getItem('umu_smart_caf_user');
    if (cachedUser) {
        try {
            const user = JSON.parse(cachedUser);
            if (nameEl) nameEl.textContent = user.name || '';
            if (roleEl) roleEl.textContent = user.role || '';
            if (avatarEl) {
                const initial = (user.name || '').charAt(0).toUpperCase();
                avatarEl.textContent = initial || '';
            }
        } catch (e) {
            console.error("Cache parse error:", e);
        }
    }

    // Step B: Fetch from API to ensure accuracy (Silent Update)
    try {
        const response = await fetch('/api/session');
        if (!response.ok) return;

        const data = await response.json();

        if (data.success && data.user) {
            // Update UI
            if (nameEl) nameEl.textContent = data.user.name || '';
            if (roleEl) roleEl.textContent = data.user.role || '';
            if (avatarEl) {
                const initial = (data.user.name || '').charAt(0).toUpperCase();
                avatarEl.textContent = initial || '';
            }

            // Sync Cache
            localStorage.setItem('umu_smart_caf_user', JSON.stringify({
                name: data.user.name,
                role: data.user.role
            }));
        }
    } catch (error) {
        // Silent fail for profile
    }
}

// Initialize everything on page load and start intervals
function startHeaderSync() {
    // Immediate calls
    updateHeaderClock();
    initializeHeaderProfile();

    // Start intervals
    setInterval(updateHeaderClock, 1000);
}

// Auto-run when script is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startHeaderSync);
} else {
    startHeaderSync();
}

// Expose globally for convenience
window.refreshHeaderProfile = initializeHeaderProfile;
