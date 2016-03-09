import kafka

print("kafka-python version: {}".format(kafka.__version__))

if kafka.__version__ == "0.9.5":
    from kafka.client import KafkaClient
    from kafka.producer import KeyedProducer
else:
    from kafka.client import SimpleClient as KafkaClient
    from kafka.producer import KeyedProducer

import json
import time


KAFKA_URL = '192.168.10.6:9092'
KAFKA_GROUP = 'kafka_python_perf'
KAFKA_TOPIC = 'raw-events'

NUM_MESSAGES = 10
SIZE_MSG = 369

k_client = KafkaClient(KAFKA_URL)
p = KeyedProducer(k_client,
                  async=False,
                  req_acks=KeyedProducer.ACK_AFTER_LOCAL_WRITE,
                  ack_timeout=2000)
messages = []
while 1:
    for i in xrange(NUM_MESSAGES):
        message = json.dumps({'msg': 'X' * SIZE_MSG})
        messages.append(message)
        if len(messages) >= 500:
            key = int(time.time() * 1000)
            p.send_messages(KAFKA_TOPIC, str(key), *messages)
            messages = []
            print("wrote 500")
    time.sleep(1)
