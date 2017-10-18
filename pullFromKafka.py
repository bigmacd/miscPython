from kafka import KafkaConsumer
from kafka import errors as kerrors
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

def setup():
    global consumer
    global runnable
    try:
        consumer = KafkaConsumer(topic, 
                                 group_id='test-consumer-group',
                                 bootstrap_servers=[brokers])
#        consumer.seek_to_beginning()
        runnable = True
    except Exception as ex:
        print (json.dumps(log.error("Unable to connect to bootstrap server {0}, {1}".format(brokers, str(ex)))))



def main():
    global consumer
    global runnable
    while(runnable):
        for message in consumer:
            auditRecord = log.audit(message.topic,
                                    message.key,
                                    message.value)
        print(json.dumps(auditRecord))        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dryrun", help="does not actually add/remove users", action="store_true")
    parser.add_argument("--broker", help="hostname:port", default='localhost:9092')
    parser.add_argument("--topic", help="topic to consume")
    args = parser.parse_args()
    brokers = args.broker
    topic = args.topic

    while runnable is False:
        setup()
        time.sleep(30) # seconds
    main()