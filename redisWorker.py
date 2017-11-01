
import redis


def process(job_id, job_data):
    print ("Processing job id({0}) with data ({1})".format(job_id, job_data))


def main(client, processing_queue, all_queue):
    while True:
        # try to fetch a job id from "<all_queue>:jobs"
        # and push it to "<processing_queue>:jobs"
        job_id = client.brpoplpush(all_queue, processing_queue)
        job_id = job_id.decode()
        if not job_id:
            continue
        # fetch the job data
        job_data = client.hmget("job:{0}".format(job_id))
        # process the job
        process(job_id, job_data)
        # cleanup the job information from redis
        client.delete("job:%s" % (job_id, ))
        client.lrem(processing_queue, 1, job_id)


if __name__ == "__main__":
    import socket
    import os

    client = redis.StrictRedis(host="192.168.182.134")
    try:
        main(client, "processing:jobs", "all:jobs")
    except KeyboardInterrupt:
        pass