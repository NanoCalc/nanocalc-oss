import os
import redis
from rq import Worker, Queue

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
listen = ["default"]

conn = redis.from_url(redis_url)

if __name__ == "__main__":
    # Create queue objects with the given connection
    queues = [Queue(name, connection=conn) for name in listen]

    # Create a Worker that processes those queues
    worker = Worker(queues, connection=conn)
    worker.work()
