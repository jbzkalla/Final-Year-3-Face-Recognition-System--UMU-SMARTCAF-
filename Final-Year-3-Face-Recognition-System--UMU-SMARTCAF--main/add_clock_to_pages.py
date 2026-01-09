import os
import re

# List of all pages with sidebars
PAGES_WITH_SIDEBAR = [
    'dashboard.html',
    'users-list.html',
    'add-user.html',
    'edit-user.html',
    'face-capture.html',
    'attendance-control.html',
    'live-attendance.html',
    'reports-dashboard.html',
    'attendance-report.html',
    'payment-report.html',
    'user-activity-report.html',
    'system-settings.html',
    'account-management.html',
    'audit-log.html',
    'payment-dashboard.html',
    'payment-list.html',
    'bulk-payment.html',
    'receipt.html',
    'model-training.html',
    'help-documentation.html',
    'contact-support.html',
]

# Clock CSS to add to styles
CLOCK_CSS = '''
        .clock {
            font-size: 1.25rem;
            font-weight: var(--font-medium);
            font-variant-numeric: tabular-nums;
        }
'''

# Clock JavaScript
CLOCK_SCRIPT = '''
    <script>
        function updateClock() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { hour12: true });
            const clockElement = document.getElementById('realtime-clock');
            if (clockElement) {
                clockElement.textContent = timeString;
            }
        }

        setInterval(updateClock, 1000);
        updateClock(); // Initial call
    </script>'''

def add_clock_to_page(filepath):
    """Add real-time clock to a page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        modified = False
        
        # Check if clock CSS already exists
        if '.clock {' not in content:
            # Add clock CSS before </style>
            content = content.replace('    </style>', CLOCK_CSS + '\n    </style>')
            modified = True
        
        # Check if clock element exists in header
        if 'id="realtime-clock"' not in content:
            # Find the header section and add clock
            # Pattern to find header title and add clock after it
            header_pattern = r'(<h1 class="header__title">.*?</h1>)'
            
            if re.search(header_pattern, content):
                # Add clock div after header title
                replacement = r'\1\n                <div class="clock" id="realtime-clock">00:00:00</div>'
                content = re.sub(header_pattern, replacement, content)
                modified = True
        
        # Check if clock script already exists
        if 'function updateClock()' not in content:
            # Add clock script before </body>
            content = content.replace('</body>', CLOCK_SCRIPT + '\n</body>')
            modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Added clock to: {filename}")
            return True
        else:
            print(f"- Skipped (already has clock): {filename}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    base_dir = r'c:\Users\HP G3\Desktop\try wee3'
    # Process all pages
    fixed_count = 0
    for filename in PAGES_WITH_SIDEBAR:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            if add_clock_to_page(filepath):
                fixed_count += 1
        else:
            print(f"! File not found: {filename}")
    
    print(f"\n✓ Added clock to {fixed_count} pages")
    print(f"- Skipped {len(PAGES_WITH_SIDEBAR) - fixed_count} pages (already had clock)")

if __name__ == '__main__':
    main()
