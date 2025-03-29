from kafka import KafkaConsumer
import json
from .es_client import insert_log

consumer = KafkaConsumer(
    "logs-topic",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

def consume_logs():
    for message in consumer:
        log = message.value
        insert_log(log)
