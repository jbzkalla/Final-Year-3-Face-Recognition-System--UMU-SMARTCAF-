import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data Directories
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
MODELS_DIR = os.path.join(DATA_DIR, "models")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# File Paths
USERS_DB_FILE = os.path.join(DATA_DIR, "users.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")
PAYMENTS_FILE = os.path.join(DATA_DIR, "payments.xlsx")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
AUDIT_LOG_FILE = os.path.join(DATA_DIR, "audit_log.json")
SUPPORT_TICKETS_FILE = os.path.join(DATA_DIR, "support_tickets.json")

# Camera Settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Security
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION_MINUTES = 15
SESSION_TIMEOUT_MINUTES = 30

# Roles
ROLE_ADMIN = "admin"
ROLE_STAFF = "staff"
ROLE_STUDENT = "student"

# Status Codes
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_WARNING = "warning"
