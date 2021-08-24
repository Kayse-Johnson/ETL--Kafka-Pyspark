import json
import random
from datetime import datetime, timezone
from kafka import KafkaProducer
from typing import Dict, Iterable
SYMBOLS = ["APPL", "TSLA", "BTC", "GM", "SONY"]
topic = 'prices'
bootstrap_server = 'kafka:9092'
def main():
    # initialise kafka producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_server,  client_id='price-streaming', value_serializer=lambda m: json.dumps(m).encode('utf-8'), api_version = (1,4,7), batch_size = 5000)
    for price in generate_n_messages(5000): # iterate through each generated price and send the message to thhe prices kafka topic
        producer.send(topic, value=price)
        producer.flush()
    producer.close()
def generate_n_messages(n: int) -> Iterable[Dict,]:
    for _ in range(n//2):
        price = {
                    "ts": datetime.now(timezone.utc).strftime(f"%Y-%m-%d %H:%M:%S.%f")[:-3], # format the date correctly
                    "symbol": random.choice(SYMBOLS),
                    "price": round(random.normalvariate(300, 50.00), 2)
                }
        yield price

if __name__ == "__main__":
    main()