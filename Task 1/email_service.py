import smtplib
from email.mime.text import MIMEText
from config import EMAIL_CONFIG
import time

def send_quote_email(user, quote, max_retries=3):
    """
    Send personalized quote email to user
    
    Args:
        user: dict with 'email', 'first_name', 'last_name'
        quote: dict with 'text' and 'author'
        max_retries: number of retry attempts if sending fails
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Get user's full name
    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    if not user_name:
        user_name = "Friend"
    
    subject = "Your Daily Motivation from MindFuel"
    
    # Simple plain text email body
    plain_body = f"""Good Morning, {user_name}!

Here's your daily dose of motivation:

"{quote['text']}"

— {quote['author']}

---
You're receiving this because you're subscribed to MindFuel daily motivation.
Have a wonderful day!
"""
    
    # Attempt to send email with retries using SSL (port 465)
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}/{max_retries}: Sending to {user['email']}...", end=" ")
            
            # Create message
            message = MIMEText(plain_body)
            message['Subject'] = subject
            message['From'] = EMAIL_CONFIG['sender_email']
            message['To'] = user['email']
            
            # Connect using SSL (port 465) - this is what works for you
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
                server.login(
                    EMAIL_CONFIG['sender_email'],
                    EMAIL_CONFIG['sender_password']
                )
                server.send_message(message)
            
            print("[SENT]")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("[AUTH FAILED]")
            return False
            
        except smtplib.SMTPRecipientsRefused:
            print("[INVALID EMAIL]")
            return False
            
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"    Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"    Failed after {max_retries} attempts")
                return False
    
    return False