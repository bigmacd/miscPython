import time
import redis
import json
import argparse


""" Follows the StackExchange best practice for creating a work queue.
    Basically push a task and publish a message that a task is there."""

def PushTask(client, queue, task, topic):    
    client.lpush(queue, task)
    client.publish(topic, queue)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--queue",   help="The queue from which workers will grab tasks")
    parser.add_argument("-t", "--task",    help="The task data")
    parser.add_argument("-o", "--topic",   help="The topic to which workers are subscribed")
    parser.add_argument("-s", "--server",    help="redis server host or IP")
    parser.add_argument("-p", 
                        "--port",    
                        help="redis server port (default is 6379)", 
                        type=int, 
                        default=6379)
    args = parser.parse_args()
    if args.queue is None
       or args.task is None
       or args.topic is None
       or args.server is None:
       parser.print_help()
    else:
        client=redis.StrictRedis(host=args.server, args.port)
        PushTask(client, args.queue, args.task, args.topic)

