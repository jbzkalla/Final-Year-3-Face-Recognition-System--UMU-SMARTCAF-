# 📘 UMU SmartCaf - User Manual

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed on your system. You can check by running:
```bash
python --version
```

### 2. Installation
1.  **Navigate to the project directory:**
    ```bash
    cd "c:/Users/HP G3/Desktop/try wee3"
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Running the System
Start the server by running the main script:
```bash
python main.py
```
You should see output indicating the server is running (usually on `http://127.0.0.1:5000`).

### 4. Accessing the Application
Open your web browser and go to:
**`http://localhost:5000`**

---

## 🕹 Using the System

### 🔐 1. Login
- **Default Credentials:**
    - **Admin:** `admin@umu.ac.ug` / `admin123`
    - **Staff Default Pass:** `staff123`
    - **Student Default Pass:** `stud123`
- Enter credentials and click **Login**.
- **Two-Factor Authentication (2FA)**:
    - If 2FA is enabled in Settings, Staff and Admins will be prompted for a verification code.
    - **Simulation Code**: Enter `233273` to verify.
- You will be redirected to the **Dashboard**.

### 👥 2. Managing Users
- Navigate to **Users** from the sidebar.
- **Add User:** Click "Add New User", fill in the details, and save.
- **Face Capture:** In the User List, click the **Camera Icon**. Take multiple photos for accuracy.
- **User Details:** Click the **Eye Icon** in the User List to see a 360-degree view of a user's profile, including their biometric status and full payment history.
- **Edit/Delete:** Use the pencil or trash icons in the action column.

### 🤖 3. Training the Model
... (No changes needed here)

### 📷 4. Marking Attendance
1.  Go to **Attendance**.
2.  Launch the **Live Attendance Monitor**.
3.  **Access Control**: The system checks the **Payment Database** in real-time. Students with a `Paid` status will see an "Access Granted" message, while others will be "Denied".

### 💬 5. Student Feedback & Complaints
- **Students**:
    1. Click **Feedback & Complaints** in the sidebar.
    2. Select a category (Service, Food Quality, Technical, General).
    3. Describe your issue or suggestion and click **Submit**.
- **Admins**:
    1. Navigate to **Student Feedback** in the sidebar.
    2. View a list of all submissions.
    3. Update the status (Pending, In Progress, Resolved) and apply filters to track resolution.

### 💳 6. Managing Payments & Finance
- **Finance Upload (New)**:
    1. Go to **Finance Upload** in the sidebar.
    2. Drag and drop your campus bank statement or Excel file.
    3. Map your file columns (e.g., ID, Name, Amount) to the system fields.
    4. Use the **Empty Template** if you want to start from scratch (Headers only: ID, Name, Dept, Amount).
    5. Preview the data and click **Confirm Import** to update the database.
- **Manual Override**:
    1. If a student pays cash or shows a physical receipt, find them in the **User List**.
    2. Click **View (Eye Icon)** to open their profile.
    3. Click **Edit Payment**.
    4. Select `Paid`, enter the amount, and save. This grants them immediate canteen access.
- **Payment List**: View and manage all transactions in the **Payment List** section.

### 📊 6. Reports
- Go to **Reports**.
- View charts for attendance trends and financial summaries.
- Click **"Export"** on specific report pages to download data as CSV or PDF.

### ⚙️ 7. Settings & Audit
- **Settings:** Configure camera index, backup intervals, etc.
- **Audit Log:** View a history of all sensitive actions (logins, deletions, exports) for security.

---

## ❓ Troubleshooting

**Q: The camera is not opening.**
A: Ensure no other application is using the camera. Check `utils/constants.py` to change `CAMERA_INDEX` if you have multiple cameras.

**Q: Face recognition is inaccurate.**
A: Capture more photos for the user in different lighting and angles. Retrain the model afterwards.

**Q: "Internal Server Error" pops up.**
A: Check the terminal window where `python main.py` is running for detailed error messages.

**Q: I forgot the admin password.**
A: For this demo version, the admin password is hardcoded in `auth/auth_service.py`. You can reset it there or use the "Forgot Password" feature if configured with a real email service.
