# ZenQuotes Email Automation System

> **Automated daily motivational quote delivery platform built for MindFuel**

A production-grade backend service that fetches inspirational quotes from ZenQuotes API and automatically delivers them to subscribed users every morning via email.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Scheduling](#-scheduling)
- [Logging](#-logging)
- [Troubleshooting](#-troubleshooting)
- [API Documentation](#-api-documentation)
- [Future Enhancements](#-future-enhancements)

---

## ✨ Features

- ✅ **Automated Quote Fetching** - Daily quotes from ZenQuotes API
- ✅ **Personalized Emails** - Customized greetings using user's name
- ✅ **Smart Retry Logic** - Handles email failures with exponential backoff (3 attempts)
- ✅ **Database Management** - PostgreSQL for user subscription data
- ✅ **Comprehensive Logging** - Daily log files with full activity tracking
- ✅ **Flexible Scheduling** - 7 AM daily delivery (customizable)
- ✅ **Error Handling** - Graceful handling of API failures and email errors
- ✅ **Scalable Architecture** - Can handle hundreds to thousands of users
- ✅ **User Preferences** - Support for daily/weekly email frequency

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.8+ |
| **Database** | PostgreSQL 16+ |
| **Email Service** | Gmail SMTP (SSL) |
| **API** | ZenQuotes API |
| **Scheduler** | Schedule library |
| **Logging** | Python logging module |

---

## 📁 Project Structure
```
zenquotes-email-service/
│
├   config.py                 # Configuration management
│   fetch.py                  # ZenQuotes API integration
│   email_service.py          # Email sending logic
│   user_service.py           # Database operations
│   logger.py                 # Logging configuration
│   scheduler.py              # Task scheduling
│
├── logs/
│   └── zenquotes_YYYYMMDD.log   # Daily log files (auto-generated)
│
├── main.py                   # Main execution script
│
├── .env                      # Environment variables (not in git)
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 📦 Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher**
```bash
  python --version
```

- **PostgreSQL 12 or higher**
  - Installed and running on localhost
  - Default port: 5432

- **Gmail Account with App Password**
  - 2-Step Verification enabled
  - App Password generated (not regular password)

- **Internet Connection**
  - For ZenQuotes API access
  - SSL port 465 accessible (for Gmail SMTP)

---

## 🚀 Installation

### Step 1: Clone or Download the Project
```bash
cd your-preferred-directory
# Place all project files here
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management
- `requests` - HTTP library for API calls
- `schedule` - Task scheduling

### Step 3: Verify Installation
```bash
python -c "import psycopg2, requests, schedule; print('All dependencies installed!')"
```

---

## ⚙️ Configuration

### Step 1: Create `.env` File

Create a `.env` file in the project root directory:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=postgres
DB_PASSWORD=your_postgres_password

# Email Configuration (SSL)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
```

### Step 2: Get Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Navigate to **App Passwords**: https://myaccount.google.com/apppasswords
4. Select:
   - **App:** Mail
   - **Device:** Other (Custom name) → "ZenQuotes Service"
5. Click **Generate**
6. Copy the 16-character password (remove spaces)
7. Paste into `.env` file as `SENDER_PASSWORD`

⚠️ **Important:** Never commit `.env` file to version control!

---

## 🗄️ Database Setup

### Step 1: Create Database
```sql
CREATE DATABASE launchpad;
```

### Step 2: Create Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    subscription_status VARCHAR(20) DEFAULT 'active',
    email_frequency VARCHAR(20) DEFAULT 'daily',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 3: Add Sample Users
```sql
INSERT INTO users (email, first_name, last_name, subscription_status, email_frequency)
VALUES 
    ('user1@example.com', 'John', 'Doe', 'active', 'daily'),
    ('user2@example.com', 'Jane', 'Smith', 'active', 'daily'),
    ('user3@example.com', 'Bob', 'Johnson', 'active', 'daily'),
    ('user4@example.com', 'Alice', 'Williams', 'inactive', 'daily');
```

### Step 4: Verify Database Setup
```bash
python check_users.py
```

**Expected output:**
```
Total users in database: 4
ACTIVE USERS WITH DAILY FREQUENCY: 4
```

---

## 🎯 Usage

### Manual Execution

Run the main script manually to send emails immediately:
```bash
python main.py
```

**What happens:**
1. Fetches daily quote from ZenQuotes API
2. Retrieves active users with `daily` frequency
3. Sends personalized email to each user
4. Logs all activity to `logs/zenquotes_YYYYMMDD.log`

**Expected output:**
```
======================================================================
STARTING DAILY QUOTE JOB
======================================================================
Step 1: Fetching quote from ZenQuotes API...
[SUCCESS] Quote fetched: "..." - Author Name

Step 2: Retrieving active users from database...
[SUCCESS] Found 4 active daily subscribers

Step 3: Sending emails to users...
----------------------------------------------------------------------
[1/4] Processing: John Doe (user1@example.com)
  Attempt 1/3: Sending to user1@example.com... [SENT]
  [SUCCESS] Email sent to user1@example.com

[...continues for each user...]

======================================================================
JOB COMPLETED - SUMMARY
======================================================================
Total users processed: 4
Emails sent successfully: 4
Emails failed: 0
Success rate: 100.0%
Duration: 12.45 seconds
======================================================================
```

---

## ⏰ Scheduling

### Automated Daily Execution

The system uses Python's `schedule` library to run automatically at 7:00 AM every day.

#### Start the Scheduler
```bash
python utils/scheduler.py
```

**What happens:**
- ✅ Scheduler starts and waits for 7:00 AM
- ✅ Displays next scheduled run time
- ✅ Executes the job automatically every day at 7:00 AM
- ✅ Logs all activity to daily log files
- ✅ Continues running until manually stopped

**Expected output:**
```
======================================================================
ZENQUOTES EMAIL SCHEDULER
======================================================================

Scheduled to run daily at 7:00 AM

Current time: 2024-11-12 15:30:45

Next scheduled run: 2024-11-13 07:00:00

======================================================================
Scheduler is running... (Press Ctrl+C to stop)
======================================================================
```

#### Running in Background

**Windows:**
```bash
# Run without console window
pythonw utils/scheduler.py
```

**Linux/Mac:**
```bash
# Run in background
nohup python utils/scheduler.py &

# Or use screen/tmux
screen -S zenquotes
python utils/scheduler.py
# Press Ctrl+A then D to detach
```

#### Stopping the Scheduler

Press `Ctrl + C` in the terminal where the scheduler is running.

#### Changing the Schedule Time

Edit `scheduler.py`, line 33:
```python
# Change from 7:00 AM to your preferred time
schedule.every().day.at("07:00").do(job_wrapper)

# Examples:
schedule.every().day.at("09:30").do(job_wrapper)  # 9:30 AM
schedule.every().day.at("18:00").do(job_wrapper)  # 6:00 PM
```

#### Important Notes

⚠️ **Computer must remain on** for the scheduler to run  
⚠️ **Don't close the terminal** (unless using background mode)  
⚠️ **Internet connection required** for API and email sending  
✅ **Scheduler automatically resumes** after temporary failures

---

## 📊 Logging

### Log File Location

All logs are stored in the `logs/` directory with the format:
```
logs/zenquotes_YYYYMMDD.log
```

**Example:** `logs/zenquotes_20241112.log`

### Log Format
```
YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE
```

**Example log entries:**
```
2024-11-12 07:00:01 - INFO - ======================================================================
2024-11-12 07:00:01 - INFO - STARTING DAILY QUOTE JOB
2024-11-12 07:00:02 - INFO - [SUCCESS] Quote fetched: "..." - Steve Jobs
2024-11-12 07:00:03 - INFO - [SUCCESS] Found 4 active daily subscribers
2024-11-12 07:00:04 - INFO - [1/4] Processing: John Doe (user1@example.com)
2024-11-12 07:00:05 - INFO -   [SUCCESS] Email sent to user1@example.com
```

### Viewing Logs
```bash
# Windows - view latest log
type logs\zenquotes_20241112.log

# Windows - open in notepad
notepad logs\zenquotes_20241112.log

# Linux/Mac
cat logs/zenquotes_20241112.log
```

### Log Levels

| Level | Description |
|-------|-------------|
| `INFO` | Normal operations, successful actions |
| `WARNING` | Non-critical issues (e.g., no users found) |
| `ERROR` | Failures (API errors, email failures) |

---

## 🔧 Troubleshooting

### Database Issues

#### Problem: "Connection failed"
**Solution:**
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Run: `python check_users.py`

#### Problem: "Table 'users' does not exist"
**Solution:**
- Run the CREATE TABLE SQL command
- Verify database name in `.env` matches

#### Problem: "No active users found"
**Solution:**
```sql
-- Check user status
SELECT * FROM users;

-- Update users to active + daily
UPDATE users 
SET subscription_status = 'active', 
    email_frequency = 'daily';
```

### API Issues

#### Problem: "Failed to fetch quote"
**Solution:**
- Check internet connection
- Verify ZenQuotes API is accessible: https://zenquotes.io/api/today
- Check logs for specific error

#### Problem: "Malformed API response"
**Solution:**
- ZenQuotes might be down (temporary)
- The script will retry on next scheduled run

### Email Issues

#### Problem: "Authentication failed"
**Solution:**
- Verify you're using **App Password**, not regular Gmail password
- Re-generate App Password in Google Account settings
- Check `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`

#### Problem: "Connection timeout"
**Solution:**
- Check if port 465 is accessible
- Temporarily disable firewall/antivirus
- Try different network (mobile hotspot)
- Contact ISP if port is blocked

#### Problem: "Some users receive email, others don't"
**Solution:**
- Check user email addresses are valid
- Look for errors in log file
- Verify user `subscription_status = 'active'`

### Scheduler Issues

#### Problem: "Scheduler stops running"
**Solution:**
- Computer went to sleep - keep computer awake
- Terminal was closed - run in background mode
- Check logs for crash errors

---

## 📡 API Documentation

### ZenQuotes API

**Endpoint:** `https://zenquotes.io/api/today`

**Response Format:**
```json
[
  {
    "q": "The only way to do great work is to love what you do.",
    "a": "Steve Jobs",
    "h": "<blockquote>...</blockquote>"
  }
]
```

**Rate Limits:**
- Free tier: No strict limits
- Recommended: 1 request per day (as per project design)

**Error Handling:**
- Timeout: 10 seconds
- Retries: None (will retry on next scheduled run)
- Fallback: None (job aborts if API fails)

---

## 🎨 Future Enhancements

Potential improvements for the project:

### User Management
- [ ] Web interface for user registration
- [ ] Unsubscribe link in emails
- [ ] Email verification on signup
- [ ] User dashboard to view quote history

### Features
- [ ] Weekly digest option (compile 7 quotes)
- [ ] Quote categories (motivation, leadership, success, etc.)
- [ ] Multiple quote sources (fallback APIs)
- [ ] Custom sending times per user
- [ ] Quote favorites/bookmarking

### Technical
- [ ] Async email sending (Celery + Redis)
- [ ] Database connection pooling
- [ ] Email open/click tracking
- [ ] Admin dashboard with statistics
- [ ] Docker containerization
- [ ] Cloud deployment (AWS Lambda, Azure Functions)
- [ ] Unit tests with pytest
- [ ] CI/CD pipeline

### Notifications
- [ ] SMS notifications (Twilio)
- [ ] Slack integration
- [ ] Discord bot
- [ ] Mobile app (React Native)

---

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **ZenQuotes API** - For providing free inspirational quotes
- **MindFuel** - For the project requirements and vision
- **PostgreSQL** - Robust database system
- **Python Community** - For excellent libraries and tools

---

## 🔐 Security Notes

### Best Practices Implemented:
✅ Environment variables for sensitive data  
✅ `.gitignore` prevents credential exposure  
✅ App passwords instead of account passwords  
✅ No hardcoded credentials in code  
✅ Secure SMTP with SSL encryption (port 465)  

### Security Recommendations:
- Never commit `.env` file to version control
- Rotate App Passwords periodically
- Use strong database passwords
- Keep dependencies updated
- Monitor log files for suspicious activity

---

## 📚 Additional Resources

- [ZenQuotes API Documentation](https://zenquotes.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Schedule Library](https://schedule.readthedocs.io/)
- [Gmail App Passwords Guide](https://support.google.com/accounts/answer/185833)

---

**Last Updated: November 2025**
