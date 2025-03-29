from kafka import KafkaConsumer
import json
from app.es_client import insert_log

consumer = KafkaConsumer(
    "logs-topic",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='log-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def consume_logs():
    print("🚀 Kafka consumer started. Waiting for messages...")
    for message in consumer:
        log = message.value
        print(f"✅ Consumed: {log}")
        insert_log(log)

if __name__ == "__main__":
    consume_logs()
