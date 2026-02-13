import redis
from rq import Queue

redis_conn = redis.Redis(host="localhost", port=6379)
video_queue = Queue("video_queue", connection=redis_conn)
