# MongoDB Config
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "webhard_project"

# Email Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"

# Flask Config
SECRET_KEY = "super_secret_key"
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"txt", "pdf", "xlsx", "docs", "zip"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
DEBUG = True