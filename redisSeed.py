import time
import redis
import json

client=redis.StrictRedis(host="192.168.182.134")
message = { "work": "do stuff", "id": 0 }

for i in range(50):
    #print(client.hset("job:{0}".format(i), "work", "do stuff"))
    message['id'] = i
    print(client.hmset("job:{0}".format(i), message))
    client.lpush("all:jobs", i)
