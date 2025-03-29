from kafka import KafkaProducer
import json
from datetime import datetime

# Helper: custom serializer for datetime
def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=default_serializer).encode('utf-8')
)

def send_log_to_kafka(log_data):
    print(f"🔼 Sending log to Kafka: {log_data}")
    producer.send("logs-topic", log_data)
