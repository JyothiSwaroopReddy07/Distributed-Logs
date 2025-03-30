from typing import List
from datetime import datetime
from .models import LogEntry
import bisect

logs: List[LogEntry] = []

def insert_sorted(entry: LogEntry):
    timestamps = [log.timestamp for log in logs]
    index = bisect.bisect(timestamps, entry.timestamp)
    logs.insert(index, entry)

def filter_logs(service: str, start: datetime, end: datetime) -> List[LogEntry]:
    return [
        log for log in logs
        if log.source == service and start <= log.timestamp <= end
    ]
