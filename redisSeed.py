import time
import redis
import json

client=redis.StrictRedis(host="192.168.182.134")
message = { "work": "do stuff", "id": 88 }

for i in range(50):
    #print(client.hset("job:{0}".format(i), "work", "do stuff"))
    print(client.hmset("job:0", message))
    client.lpush("all:jobs", i)
