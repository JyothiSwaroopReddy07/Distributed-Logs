import requests
import random
from datetime import datetime, timedelta
import time

# Configuration
ENDPOINT = "http://localhost:8001/logs"
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
SOURCES = ["frontend", "backend", "auth-service", "db", "cron-job", "api-gateway"]
MESSAGES = [
    "User logged in",
    "File not found",
    "Database connection failed",
    "Token expired",
    "Retrying request",
    "Cache miss",
    "Permission denied",
    "Request timed out"
]

def generate_log():
    now = datetime.utcnow()

    # Random time within the last 30 days
    random_minutes = random.randint(0, 60 * 24 * 30)
    timestamp = now - timedelta(minutes=random_minutes)

    log = {
        "timestamp": timestamp.isoformat(),
        "level": random.choice(LOG_LEVELS),
        "message": random.choice(MESSAGES),
        "source": random.choice(SOURCES)
    }
    return log

def send_logs(count=100, delay=0.1):
    for _ in range(count):
        log = generate_log()
        response = requests.post(ENDPOINT, json=log)
        print(f"Sent log at {log['timestamp']} | Status: {response.status_code}")
        time.sleep(delay)

if __name__ == "__main__":
    send_logs(count=100, delay=0.05)  # Sends 100 logs with 50ms delay
