import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD')
}

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT', '485')),
    'sender_email': os.getenv('SENDER_EMAIL'),
    'sender_password': os.getenv('SENDER_PASSWORD')
}

# Print config (without passwords) for debugging
def print_db_config():
    print("Database Configuration:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Password: {'*' * len(DB_CONFIG['password']) if DB_CONFIG['password'] else 'NOT SET'}")

def print_email_config():
    print("Email Configuration:")
    print(f"  SMTP Server: {EMAIL_CONFIG['smtp_server']}")
    print(f"  SMTP Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"  Sender Email: {EMAIL_CONFIG['sender_email']}")
    print(f"  Password: {'*' * len(EMAIL_CONFIG['sender_password']) if EMAIL_CONFIG['sender_password'] else 'NOT SET'}")