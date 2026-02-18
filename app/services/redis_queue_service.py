from app.connection.queue_conn import video_queue


def check_queue_is_empty():
    return video_queue.is_empty()

def check_queue_count():
    return video_queue.count

def get_failed_jobs():
    print(video_queue.failed_job_registry)
