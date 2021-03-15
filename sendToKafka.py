from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers = ["localhost:9092"],
                         client_id = "my_client_id")

#print(producer.bootstrap_connected())

index = 0
while True:
    ack = producer.send('test_topic', 
                      value = bytes(f'Message Number: {index}', 'utf-8'))
                      #key = bytes('just a key', 'utf-8'))
                        #, headers=None, partition=None, timestamp_ms=None)

    #metadata = ack.get()
    #print(metadata.topic)
    #print(metadata.partition)

    # producer.flush()
    # print(producer.metrics())
    index += 1
    time.sleep(5)
