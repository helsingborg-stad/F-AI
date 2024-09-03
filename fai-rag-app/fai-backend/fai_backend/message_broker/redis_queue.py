from typing import Optional, Any

import redis
from rq import Queue
from rq.job import Job
from rq.job import JobStatus


class RedisQueue:
    def __init__(self, host, port,
                 password: str | None = None,
                 username: str | None = None,
                 db: int = 0, queue_name: str = 'default') -> None:
        self.redis = redis.StrictRedis(host, port, password, db, username)
        self.queue = Queue(queue_name, connection=self.redis)

    def enqueue(self, func, *args, **kwargs) -> Job:
        return self.queue.enqueue(func, *args, **kwargs)

    def get_status(self, job_id: str) -> JobStatus:
        job = Job.fetch(job_id, connection=self.redis)
        return job.get_status()

    def get_result(self, job_id: str) -> Optional[Any]:
        job = Job.fetch(job_id, connection=self.redis)
        return job.return_value()
