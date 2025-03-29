import requests
import random
from datetime import datetime, timedelta
import time

# Configuration (match the POST port)
ENDPOINT = "http://localhost:8001/logs"
SOURCES = ["frontend", "backend", "auth-service", "db", "cron-job", "api-gateway"]

def random_date_range():
    now = datetime.utcnow()
    start_offset = random.randint(1, 29)  # between 1 and 29 days ago
    duration_minutes = random.randint(1440, 21600)  # window of 1 day to 15 days

    start = now - timedelta(days=start_offset, minutes=random.randint(0, 1440))
    end = start + timedelta(minutes=duration_minutes)
    return start, end

def fetch_logs(iterations=10, delay=0.3):
    for _ in range(iterations):
        source = random.choice(SOURCES)
        start, end = random_date_range()

        params = {
            "service": source,
            "start": start.isoformat(),
            "end": end.isoformat()
        }

        try:
            response = requests.get(ENDPOINT, params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ [{source}] {start} → {end} — {len(data)} log(s) found")
            else:
                print(f"❌ [{source}] {response.status_code}: {response.text}")
        except Exception as e:
            print(f"🚨 Request failed: {e}")

        time.sleep(delay)

if __name__ == "__main__":
    fetch_logs(iterations=20, delay=0.25)
