import os

import redis
from rq import Queue, Worker


redis_connection = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

queues = [Queue("downloads", connection=redis_connection)]

if __name__ == "__main__":
    worker = Worker(queues, connection=redis_connection)
    worker.work(with_scheduler=True)