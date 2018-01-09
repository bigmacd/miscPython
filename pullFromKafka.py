from kafka import KafkaClient, SimpleConsumer
from kafka import errors as kerrors
import json
import argparse
import datetime
import time


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


def setup(brokers, topic, group):
    consumer = None
    try:
        client = KafkaClient(brokers)
	consumer = SimpleConsumer(client, 
                                  group,
                                  topic)
    except Exception as ex:
        print (json.dumps(log.error("Unable to connect to bootstrap server {0}, {1}".format(brokers, str(ex)))))

    return consumer



def main(consumer, topic):
    if consumer is not None:
        for message in consumer:
            auditRecord = log.audit(topic,
                                    message.message.key,
                                    message.message.value)
        print(json.dumps(auditRecord))        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker", help="hostname:port", default='localhost:9092')
    parser.add_argument("--topic", help="topic to consume")
    parser.add_argument("--group", help="group_id string")
    args = parser.parse_args()
    brokers = args.broker
    topic = args.topic
    group = args.group

    main(setup(args.broker, args.topic, args.group), topic)
