from confluent_kafka import Consumer, KafkaError
import json
import argparse
import datetime
import time

consumer = None
runnable = False

class logger(): # implements the document/mapping definition
    def __init__(self):
        pass
    def getTimestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def audit(self, topic, key, value):
        return { "topic" : topic, "key" : key, "value": value, "timestamp": self.getTimestamp() }
    def error(self, message):
        return { "topic": "Error", "key": "error", "value": message , "timestamp": self.getTimestamp() }

log = logger()

def setup(options, topic):
    global consumer
    global runnable
    try:
        consumer = Consumer(options)
        consumer.subscribe([topic])
        runnable = True
    except Exception as ex:
        print (json.dumps(log.error("Unable to connect to bootstrap server {0}, {1}".format(brokers, str(ex)))))



def main():
    global consumer
    global runnable
    while(runnable):
        message = consumer.poll()
        if message is not None:
            if not message.error():
                auditRecord = log.audit(message.topic(),
                                        message.key().decode('utf-8'),
                                        message.value().decode('utf-8'))
                print(json.dumps(auditRecord))
        else:
            print(json.dumps(log.error("Poller received an empty message")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dryrun", help="does not actually add/remove users", action="store_true")
    parser.add_argument("--broker", help="hostname:port", default='localhost:9092')
    parser.add_argument("--topic", help="topic to consume")
    args = parser.parse_args()
    brokers = args.broker
    topic = args.topic

    options = {
        'bootstrap.servers': brokers,
        'group.id': 'test-consumer-group',
        'default.topic.config': { 'auto.offset.reset': 'smallest'}
    }

    setup(options, topic)
    while runnable is False:
        time.sleep(30) # seconds
        setup(options, topic)
    main()
    consumer.close()