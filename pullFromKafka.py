from kafka import KafkaConsumer
from kafka import errors as kerrors
import json
import argparse
import datetime

consumer = None
messageList = []

class logger(): # implements the document/mapping definition
    def __init__(self):
        pass
    def getTimestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def audit(self, topic, key, value):
        item = { "topic" : topic, "key" : key, "value": value, "timestamp": self.getTimestamp() }
        messageList.append(item)

log = logger()

def setup():
    global consumer
    try:
        consumer = KafkaConsumer(topic, 
                                 bootstrap_servers=[brokers])
    except kerrors.NoBrokersAvailable as ex:
        print("Unable to connect to bootstrap servers in {0:s}".format(brokers))
        raise


def main():
    global consumer
    while(True):
        for message in consumer:
            log.audit(message.topic,
                      message.key,
                      message.value)
        print(json.dumps(messageList))        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dryrun", help="does not actually add/remove users", action="store_true")
    parser.add_argument("--broker", help="hostname:port", default='localhost:9092')
    parser.add_argument("--topic", help="topic to consume")
    args = parser.parse_args()
    brokers = args.broker
    topic = args.topic

    setup()
    main()