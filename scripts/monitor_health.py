#!/usr/bin/env python3
"""
UMAJA-Core Automated Health Check Monitoring
Runs health checks on a schedule and alerts on failures
"""

import sys
import time
import json
import smtplib
import tempfile
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import os

# Configuration
CHECK_INTERVAL = 300  # 5 minutes
ALERT_THRESHOLD = 3  # Alert after 3 consecutive failures
LOG_FILE = os.path.join(tempfile.gettempdir(), "umaja_health_monitor.log")

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Append to log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def run_health_check():
    """Run the backend URL verification script"""
    script_path = os.path.join(os.path.dirname(__file__), 'verify_backend_url.py')
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check exit code (0 = success, 1 = failure)
        return result.returncode == 0, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        return False, "", "Health check timed out after 30 seconds"
    except Exception as e:
        return False, "", str(e)

def send_alert(failure_count, last_error):
    """Send alert notification (placeholder - implement based on your needs)"""
    alert_message = f"""
    🚨 UMAJA Backend Health Alert 🚨
    
    Status: OFFLINE
    Consecutive Failures: {failure_count}
    Last Error: {last_error}
    Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    Action Required:
    1. Check Railway deployment: https://railway.app/dashboard
    2. Verify backend logs
    3. Run manual test: python3 scripts/verify_backend_url.py
    """
    
    log(f"⚠️  ALERT: {alert_message}")
    
    # TODO: Implement actual alerting (email, Slack, Discord, etc.)
    # Example email implementation (commented out - configure as needed):
    """
    # Email configuration
    EMAIL_FROM = os.environ.get('ALERT_EMAIL_FROM', 'alerts@umaja.org')
    EMAIL_TO = os.environ.get('ALERT_EMAIL_TO', 'admin@umaja.org')
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    
    if SMTP_USER and SMTP_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_FROM
            msg['To'] = EMAIL_TO
            msg['Subject'] = '🚨 UMAJA Backend Health Alert'
            msg.attach(MIMEText(alert_message, 'plain'))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            log("✅ Alert email sent successfully")
        except Exception as e:
            log(f"❌ Failed to send alert email: {e}")
    """
    
    # Write alert to file for external monitoring
    alert_file = os.path.join(tempfile.gettempdir(), "umaja_health_alert.json")
    with open(alert_file, 'w') as f:
        json.dump({
            'status': 'ALERT',
            'failure_count': failure_count,
            'last_error': last_error,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)

def main():
    """Main monitoring loop"""
    log("🚀 Starting UMAJA Health Check Monitor")
    log(f"📊 Check interval: {CHECK_INTERVAL} seconds")
    log(f"⚠️  Alert threshold: {ALERT_THRESHOLD} consecutive failures")
    log(f"📝 Log file: {LOG_FILE}")
    
    consecutive_failures = 0
    last_status = None
    
    try:
        while True:
            log("🔍 Running health check...")
            
            success, stdout, stderr = run_health_check()
            
            if success:
                if last_status == False:
                    log("✅ Backend RECOVERED - Now online")
                    consecutive_failures = 0
                else:
                    log("✅ Backend healthy")
                
                last_status = True
                consecutive_failures = 0
                
            else:
                consecutive_failures += 1
                log(f"❌ Health check failed (attempt {consecutive_failures}/{ALERT_THRESHOLD})")
                
                if stderr:
                    log(f"   Error: {stderr[:200]}")
                
                if consecutive_failures >= ALERT_THRESHOLD:
                    log(f"🚨 ALERT THRESHOLD REACHED - Sending alert")
                    send_alert(consecutive_failures, stderr or "Unknown error")
                
                last_status = False
            
            # Wait before next check
            log(f"⏳ Waiting {CHECK_INTERVAL} seconds until next check...")
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        log("👋 Monitoring stopped by user")
        sys.exit(0)
    except Exception as e:
        log(f"💥 Monitoring error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
