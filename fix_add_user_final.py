# Simple script to fix add-user.html
with open('add-user.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change title
content = content.replace('<title>Dashboard - UMU SmartCaf</title>', '<title>Add User - UMU SmartCaf</title>')

# 2. Change active nav link
content = content.replace('href="dashboard.html" class="nav__link active"', 'href="dashboard.html" class="nav__link"')
content = content.replace('href="users-list.html" class="nav__link"', 'href="users-list.html" class="nav__link active"')

# 3. Change header title  
content = content.replace('<h1 class="header__title">Overview</h1>', '<h1 class="header__title">Add New User</h1>')

# 4. Remove fetchDashboardStats function and its call
import re
content = re.sub(r'async function fetchDashboardStats\(\) \{[^}]+\}[^}]+\}[^}]+\}', '', content, flags=re.DOTALL)
content = content.replace('fetchDashboardStats(); // Fetch stats on load', '')
content = content.replace('// setInterval(fetchDashboardStats, 30000); // Refresh every 30 seconds', '')

# 5. Replace dashboard content with form
dashboard_content_pattern = r'(</header>\s*<!-- Status Cards -->)(.*?)(</main>)'
form_content = r'''\1

            <!-- Add User Form -->
            <div class="form-container">
                <form class="user-form">
                    <div class="form-group">
                        <label class="form-label">User ID (Auto-generated)</label>
                        <input type="text" class="form-input" value="2023-B291-11711" readonly style="opacity: 0.7; cursor: not-allowed;">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Full Name</label>
                        <input type="text" class="form-input" placeholder="Enter full name" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email Address</label>
                        <input type="email" class="form-input" placeholder="Enter email address" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Department</label>
                        <select class="form-select" required>
                            <option value="" disabled selected>Select Department</option>
                            <option value="CS">Computer Science</option>
                            <option value="ENG">Engineering</option>
                            <option value="BUS">Business</option>
                            <option value="EDU">Education</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Role</label>
                        <select class="form-select" required>
                            <option value="Student" selected>Student</option>
                            <option value="Staff">Staff</option>
                            <option value="Admin">Admin</option>
                        </select>
                    </div>
                    <div class="form-actions">
                        <a href="users-list.html" class="btn btn-secondary">Cancel</a>
                        <button type="submit" class="btn btn-primary">Save User</button>
                    </div>
                </form>
            </div>
\3'''

content = re.sub(dashboard_content_pattern, form_content, content, flags=re.DOTALL)

# 6. Add form styles before </style>
form_styles = '''
        /* Form Container */
        .form-container {
            background-color: var(--card-bg);
            backdrop-filter: blur(8px);
            border: var(--glass-border);
            border-radius: 1rem;
            padding: 2rem;
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: var(--font-medium);
            font-size: var(--small-font-size);
        }

        .form-input,
        .form-select {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: var(--glass-border);
            background-color: var(--glass-bg);
            color: var(--white-color);
            outline: none;
            font-family: var(--body-font);
        }

        .form-select option {
            background-color: #333;
        }

        .form-input:focus,
        .form-select:focus {
            border-color: var(--white-color);
        }

        .form-actions {
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
            margin-top: 2rem;
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: var(--font-medium);
            cursor: pointer;
            border: none;
            text-decoration: none;
            display: inline-block;
            transition: opacity 0.3s;
        }

        .btn-primary {
            background-color: var(--white-color);
            color: var(--black-color);
        }

        .btn-secondary {
            background-color: transparent;
            border: 1px solid var(--white-color);
            color: var(--white-color);
        }

        .btn:hover {
            opacity: 0.9;
        }
'''

content = content.replace('    </style>', form_styles + '\n    </style>')

with open('add-user.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed add-user.html successfully")
