import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def get_db_connection():
    """Creates and returns database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"[FAILED] Database connection failed: {str(e)}")
        raise

def get_active_users(frequency='daily'):
    """
    Fetch users who should receive emails
    frequency: 'daily' or 'weekly'
    Returns: list of user dictionaries
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT user_id, email, first_name, last_name, email_frequency
            FROM users
            WHERE subscription_status = 'active'
            AND email_frequency = %s
        """
        
        cursor.execute(query, (frequency,))
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        print(f"[SUCCESS] Retrieved {len(users)} active users with {frequency} frequency")
        return users
        
    except Exception as e:
        print(f"[FAILED] Error fetching users: {str(e)}")
        return []