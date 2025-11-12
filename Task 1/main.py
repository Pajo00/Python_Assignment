from fetch import fetch_daily_quote
from user_service import get_active_users
from email_service import send_quote_email
from logger import setup_logger, get_logger
from datetime import datetime

def run_daily_quote_job():
    """Main function that orchestrates the daily quote sending"""
    
    # Setup logging
    logger = setup_logger()
    
    logger.info("=" * 70)
    logger.info("STARTING DAILY QUOTE JOB")
    logger.info("=" * 70)
    
    # Statistics for tracking
    stats = {
        'total_users': 0,
        'emails_sent': 0,
        'emails_failed': 0,
        'failed_users': [],
        'start_time': datetime.now()
    }
    
    # Step 1: Fetch quote from ZenQuotes API
    logger.info("Step 1: Fetching quote from ZenQuotes API...")
    quote = fetch_daily_quote()
    
    if not quote:
        logger.error("[FAILED] Could not fetch quote from API. Aborting job.")
        return
    
    logger.info(f"[SUCCESS] Quote fetched: \"{quote['text']}\" - {quote['author']}")
    print()
    
    # Step 2: Get active users from database
    logger.info("Step 2: Retrieving active users from database...")
    users = get_active_users(frequency='daily')
    stats['total_users'] = len(users)
    
    if not users:
        logger.warning("[WARNING] No active users found with daily frequency")
        logger.info("Job completed - nothing to send")
        return
    
    logger.info(f"[SUCCESS] Found {len(users)} active daily subscribers")
    print()
    
    # Step 3: Send emails to each user
    logger.info("Step 3: Sending emails to users...")
    logger.info("-" * 70)
    
    for index, user in enumerate(users, 1):
        user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        logger.info(f"[{index}/{len(users)}] Processing: {user_name} ({user['email']})")
        
        try:
            success = send_quote_email(user, quote)
            
            if success:
                stats['emails_sent'] += 1
                logger.info(f"  [SUCCESS] Email sent to {user['email']}")
            else:
                stats['emails_failed'] += 1
                stats['failed_users'].append(user['email'])
                logger.error(f"  [FAILED] Could not send email to {user['email']}")
        
        except Exception as e:
            stats['emails_failed'] += 1
            stats['failed_users'].append(user['email'])
            logger.error(f"  [ERROR] Unexpected error for {user['email']}: {str(e)}")
        
        print()
    
    # Step 4: Log summary
    stats['end_time'] = datetime.now()
    stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()
    
    logger.info("=" * 70)
    logger.info("JOB COMPLETED - SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total users processed: {stats['total_users']}")
    logger.info(f"Emails sent successfully: {stats['emails_sent']}")
    logger.info(f"Emails failed: {stats['emails_failed']}")
    
    if stats['failed_users']:
        logger.warning(f"Failed recipients: {', '.join(stats['failed_users'])}")
    
    logger.info(f"Success rate: {(stats['emails_sent']/stats['total_users']*100):.1f}%" if stats['total_users'] > 0 else "N/A")
    logger.info(f"Duration: {stats['duration']:.2f} seconds")
    logger.info(f"Quote of the day: \"{quote['text']}\" - {quote['author']}")
    logger.info("=" * 70)

if __name__ == "__main__":
    run_daily_quote_job()