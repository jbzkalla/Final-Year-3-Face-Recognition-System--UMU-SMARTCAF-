# Script to create users-list.html from dashboard template
import re

# Read dashboard.html as template
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change title
content = content.replace('<title>Dashboard - UMU SmartCaf</title>', '<title>User Management - UMU SmartCaf</title>')

# Change active nav link
content = content.replace('href="dashboard.html" class="nav__link active"', 'href="dashboard.html" class="nav__link"')
content = content.replace('href="users-list.html" class="nav__link"', 'href="users-list.html" class="nav__link active"')

# Change header title
content = content.replace('<h1 class="header__title">Overview</h1>', '<h1 class="header__title">User Management</h1>')

# Add user management specific styles before the closing </style> tag
user_styles = '''
        /* User Management Specific Styles */
        .controls-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .tabs {
            display: flex;
            gap: 0.5rem;
            background-color: var(--glass-bg);
            padding: 0.25rem;
            border-radius: 0.5rem;
            border: var(--glass-border);
        }

        .tab-btn {
            padding: 0.5rem 1rem;
            border: none;
            background: none;
            color: var(--white-color);
            cursor: pointer;
            border-radius: 0.25rem;
            font-weight: var(--font-medium);
            transition: background-color 0.3s;
        }

        .tab-btn.active {
            background-color: hsla(0, 0%, 100%, 0.2);
        }

        .search-filter {
            display: flex;
            gap: 1rem;
        }

        .search-input {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            border: var(--glass-border);
            background-color: var(--glass-bg);
            color: var(--white-color);
            outline: none;
        }

        .filter-select {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            border: var(--glass-border);
            background-color: var(--glass-bg);
            color: var(--white-color);
            outline: none;
        }

        .filter-select option {
            background-color: #333;
        }

        .btn-add {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            background-color: var(--white-color);
            color: var(--black-color);
            font-weight: var(--font-medium);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: opacity 0.3s;
        }

        .btn-add:hover {
            opacity: 0.9;
        }

        /* Table */
        .table-container {
            background-color: var(--card-bg);
            backdrop-filter: blur(8px);
            border: var(--glass-border);
            border-radius: 1rem;
            padding: 1rem;
            overflow-x: auto;
        }

        table {
            width: 100%;\n            border-collapse: collapse;
            min-width: 800px;
        }

        th,
        td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid hsla(0, 0%, 100%, 0.1);
        }

        th {
            background-color: var(--table-header-bg);
            font-weight: var(--font-semi-bold);
            color: var(--white-color);
        }

        tr:last-child td {
            border-bottom: none;
        }

        .status-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 1rem;
            font-size: var(--small-font-size);
            font-weight: var(--font-medium);
        }

        .status-registered {
            background-color: hsla(120, 100%, 30%, 0.4);
            color: #8aff8a;
        }

        .status-pending {
            background-color: hsla(40, 100%, 50%, 0.4);
            color: #ffda8a;
        }

        .action-btn {
            background: none;
            border: none;
            color: var(--white-color);
            cursor: pointer;
            font-size: 1.2rem;
            margin-right: 0.5rem;
            transition: color 0.3s;
        }

        .action-btn:hover {
            color: #ffd700;
        }

        .action-btn.delete:hover {
            color: #ff6b6b;
        }
'''

content = content.replace('    </style>', user_styles + '\n    </style>')

# Replace the main content section (everything after </header> and before </main>)
# Find the pattern for the status cards and replace with user management content
pattern = r'(</header>\s*)(.*?)(\s*</main>)'

replacement_content = r'''\1
            <!-- Header with Add Button -->
            <div class="header">
                <h1 class="header__title">User Management</h1>
                <a href="add-user.html" class="btn-add">
                    <i class="ri-user-add-line"></i>
                    Add New User
                </a>
            </div>

            <!-- Controls -->
            <div class="controls-bar">
                <div class="tabs">
                    <button class="tab-btn active">Students</button>
                    <button class="tab-btn">Staff</button>
                    <button class="tab-btn">Admins</button>
                </div>
                <div class="search-filter">
                    <input type="text" placeholder="Search users..." class="search-input">
                    <select class="filter-select">
                        <option value="">All Departments</option>
                        <option value="CS">Computer Science</option>
                        <option value="ENG">Engineering</option>
                        <option value="BUS">Business</option>
                    </select>
                </div>
            </div>

            <!-- Users Table -->
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Role</th>
                            <th>Department</th>
                            <th>Face Data</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>2023-B291-11709</td>
                            <td>Kato Joseph</td>
                            <td>Student</td>
                            <td>Computer Science</td>
                            <td><span class="status-badge status-registered">Registered</span></td>
                            <td>
                                <button class="action-btn" title="View"><i class="ri-eye-line"></i></button>
                                <a href="edit-user.html" class="action-btn" title="Edit"><i class="ri-pencil-line"></i></a>
                                <a href="face-capture.html" class="action-btn" title="Capture Face"><i class="ri-camera-lens-line"></i></a>
                                <button class="action-btn delete" title="Delete"><i class="ri-delete-bin-line"></i></button>
                            </td>
                        </tr>
                        <tr>
                            <td>2023-B291-11710</td>
                            <td>Jane Doe</td>
                            <td>Student</td>
                            <td>Business</td>
                            <td><span class="status-badge status-pending">Pending</span></td>
                            <td>
                                <button class="action-btn" title="View"><i class="ri-eye-line"></i></button>
                                <a href="edit-user.html" class="action-btn" title="Edit"><i class="ri-pencil-line"></i></a>
                                <a href="face-capture.html" class="action-btn" title="Capture Face"><i class="ri-camera-lens-line"></i></a>
                                <button class="action-btn delete" title="Delete"><i class="ri-delete-bin-line"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
\3'''

content = re.sub(pattern, replacement_content, content, flags=re.DOTALL)

# Remove the dashboard-specific JavaScript
content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)

# Write the new users-list.html
with open('users-list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Created users-list.html successfully")
