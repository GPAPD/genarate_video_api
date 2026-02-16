import redis
from rq import Queue
import os

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_conn = redis.Redis(host=redis_host, port=redis_port)
video_queue = Queue("video_queue", connection=redis_conn)