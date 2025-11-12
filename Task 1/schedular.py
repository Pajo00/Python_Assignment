import schedule
import time
from main import run_daily_quote_job
from logger import setup_logger, get_logger
from datetime import datetime

def job_wrapper():
    """Wrapper function that runs the job and handles any errors"""
    logger = get_logger()
    try:
        run_daily_quote_job()
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        print(f"✗ Job failed: {str(e)}")

def start_scheduler():
    """Start the scheduler to run job daily at 7 AM"""
    
    # Setup logging
    logger = setup_logger()
    
    print()
    print("=" * 70)
    print("ZENQUOTES EMAIL SCHEDULER")
    print("=" * 70)
    print()
    print("Scheduled to run daily at 7:00 AM")
    print()
    print("Current time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Schedule job for 7 AM daily
    schedule.every().day.at("07:00").do(job_wrapper)
    
    # Show next scheduled run time
    next_run = schedule.next_run()
    if next_run:
        print(f"Next scheduled run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()
    print("=" * 70)
    print("Scheduler is running... (Press Ctrl+C to stop)")
    print("=" * 70)
    print()
    
    logger.info("Scheduler started - job will run daily at 7:00 AM")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("Scheduler stopped by user")
        print("=" * 70)
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    start_scheduler()