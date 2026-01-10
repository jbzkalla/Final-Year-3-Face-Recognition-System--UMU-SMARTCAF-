# KATO JOSEPH BWANIKA.
# REG:2023-B291-11709.

# UMU SmartCaf - Smart Cafeteria Management System

UMU SmartCaf is a comprehensive web-based application designed to manage cafeteria operations at Uganda Martyrs University. It integrates **Face Recognition** for attendance and payments, providing a seamless and secure experience for students and staff.

### Recent Enhancements
- **Student Feedback & Complaints System**: Integrated ticket management for students and a centralized dashboard for administrators.
- **Premium Dark Theme & Glassmorphism**: A modern, sleek UI design with high visibility and responsive components.
- **Finance Template Refinement**: Simplified, headers-only CSV/Excel templates for bulk data import.
- **Automated Reporting with Branding**: Professional PDF and CSV reports featuring the university logo.

## System Architecture
The application follows a modular **Model-View-Controller (MVC)** pattern:
- **Frontend (View):** HTML5, CSS3 (Vanilla), JavaScript (Fetch API).
- **Backend (Controller & Model):** Python (Flask), OpenCV (Face Recognition).
- **Data Layer:** File-based storage (JSON, CSV, Excel) for portability and simplicity.

---

## Folder Structure & File Descriptions

### 1. Root Directory (Frontend & Entry Point)
Contains the user interface files and the main server script.

#### Core Python File
- **`main.py`**: The entry point of the application. It initializes the Flask server, registers all blueprints (modules), and serves the frontend files.

#### HTML Pages (Frontend)
- **Authentication**
    - `login.html`: User login page with role detection.
    - `register.html`: New user registration page.
    - `forgot-password.html`: Password recovery interface.
    - `logout-confirmation.html`: Confirmation screen upon logging out.
    - `training-auth.html`: Security check before accessing model training.

- **Dashboard**
    - `dashboard.html`: Main administrative dashboard showing key statistics and quick links.

- **User Management**
    - `users-list.html`: Displays all registered users with search and filter options.
    - `user-details.html`: Comprehensive 360-view of a user's status, biometric data, and payment history.
    - `add-user.html`: Form to register a new user manually.
    - `edit-user.html`: Form to update existing user details.
    - `face-capture.html`: Interface to capture face images for the recognition model.

- **Attendance**
    - `attendance-control.html`: Dashboard to start/stop attendance sessions.
    - `live-attendance.html`: Real-time face recognition interface for marking attendance. Access is granted based on the **Payment Database**.

- **Payments & Finance**
    - `payment-dashboard.html`: Overview of financial stats (Total Collected, Pending) powered by the new Payment Engine.
    - `payment-list.html`: List of all payment records with quick status updates.
    - `finance-upload.html`: High-performance interface for importing Excel/CSV finance records with column mapping and validation.
    - `bulk-payment.html`: Legacy interface to upload files for bulk payment updates.
    - `receipt.html`: Template for generating payment receipts.

- **Reports**
    - `reports-dashboard.html`: Central hub for all system reports.
    - `attendance-report.html`: Detailed attendance logs with export options.
    - `payment-report.html`: Financial statements and transaction history.
    - `user-activity-report.html`: Logs of individual user actions.

- **Administration & Security**
    - `system-settings.html`: Configuration for backup, camera, and system preferences.
    - `account-management.html`: Manage admin accounts and roles.
    - `audit-log.html`: Security logs showing who did what and when.
    - `model-training.html`: Interface to train the face recognition model.

- **Support**
    - `contact-support.html`: Form to submit support tickets.
    - `help-documentation.html`: User guides and FAQs.
    - `error.html`: Generic error page for 404/500 errors.

---

### 2. Backend Modules (Python)
The backend is organized into domain-specific folders.

#### `auth/` (Authentication)
- `auth_controller.py`: Handles login, registration, and logout requests.
- `auth_service.py`: Business logic for verifying credentials and managing sessions.
- `password_utils.py`: Utilities for hashing and verifying passwords.

#### `dashboard/` (Dashboard)
- `dashboard_controller.py`: Serves data for the main dashboard.
- `dashboard_service.py`: Aggregates statistics (total users, attendance count, etc.).

#### `users/` (User Management)
- `user_controller.py`: API endpoints for CRUD operations on users.
- `user_service.py`: Logic for creating, updating, and deleting users.
- `face_capture_service.py`: Handles capturing and saving face images from the camera.
- `user_validator.py`: Validates user input data.

#### `attendance/` (Attendance & Recognition)
- `attendance_controller.py`: Endpoints for starting sessions and marking attendance.
- `attendance_service.py`: Logic to record attendance in CSV files.
- `recognition_service.py`: Core face recognition logic using OpenCV.
- `session_manager.py`: Manages active attendance sessions.

#### `payments/` (Payments)
- `payment_controller.py`: Handles payment updates and receipt generation.
- `payment_service.py`: Manages user balances and transaction records.
- `excel_importer.py`: Logic to parse uploaded Excel files for bulk payments.

#### `reports/` (Reports)
- `report_controller.py`: Endpoints to fetch aggregated data for reports.
- `report_service.py`: Generates summaries for attendance, payments, and activity.

#### `training/` (Model Training)
- `training_controller.py`: API to trigger model training.
- `training_service.py`: Manages the background training process.
- `model_manager.py`: Uses OpenCV to train the LBPH face recognizer.

#### `admin/` (Administration)
- `settings_controller.py`: Endpoints for saving system settings.
- `settings_service.py`: Manages `settings.json`.
- `account_service.py`: Logic for admin account management.

#### `security/` (Security)
- `security_controller.py`: Endpoints for audit logs.
- `audit_logger.py`: Logs system events to `audit_log.json`.
- `role_guard.py`: Decorators for role-based access control (RBAC).
- `lockout_manager.py`: Prevents brute-force attacks.

#### `support/` (Support)
- `support_controller.py`: Handles ticket submissions.
- `ticket_service.py`: Manages support tickets and mock email notifications.

#### `data/` (Data Access Layer)
- `file_manager.py`: Helpers for reading/writing JSON and files.
- `excel_repository.py`: Helpers for Excel operations.
- `image_repository.py`: Manages storage of user face images.
- **Storage Files**: `users.json`, `attendance.csv`, `audit_log.json`, etc. (Created automatically).

#### `utils/` (Utilities)
- `constants.py`: Global configuration and paths.
- `camera_utils.py`: OpenCV camera wrappers.
- `time_utils.py`: Date and time formatting helpers.
- `id_generator.py`: Generates unique IDs for users and tickets.

---

## Default Credentials
For the initial system setup, the following default credentials are provided:
- **System Admin**: 
  - Email: `admin@umu.ac.ug`
  - Password: `admin123`
- **Staff**:
  - Default Password: `staff123`
- **Student**:
  - Default Password: `stud123`

- **Two-Factor Authentication (2FA)**:
  - Simulation Code: `233273`

*Note: Passwords can be changed by users during signup or in their account settings.*

## Requirements
- Python 3.8+
- Flask
- OpenCV (`opencv-python`)
- NumPy
- Pandas
- OpenPyXL

See `requirements.txt` for the full list.
