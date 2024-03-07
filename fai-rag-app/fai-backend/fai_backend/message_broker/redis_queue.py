from typing import Optional, Any

import redis
from rq import Queue
from rq.job import Job
from rq.job import JobStatus
from fai_backend.message_broker.interface import IMessageQueue


class RedisQueue(IMessageQueue):
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0,
                 queue_name: str = 'default'):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        self.queue = Queue(queue_name, connection=self.redis)

    def enqueue(self, func, *args, **kwargs) -> Job:
        return self.queue.enqueue(func, *args, **kwargs)

    def get_status(self, job_id: str) -> JobStatus:
        job = Job.fetch(job_id, connection=self.redis)
        return job.get_status()

    def get_result(self, job_id: str) -> Optional[Any]:
        job = Job.fetch(job_id, connection=self.redis)
        return job.return_value()
