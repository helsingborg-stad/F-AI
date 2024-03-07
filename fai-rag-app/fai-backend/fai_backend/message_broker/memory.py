from typing import Optional, Any

import fakeredis
from rq import Queue
from rq.job import Job

from fai_backend.message_broker.interface import IMessageQueue, JobStatus


class MemoryQueue(IMessageQueue):
    def __init__(self):
        self.fake_redis = fakeredis.FakeStrictRedis()
        self.queue = Queue(is_async=False, connection=self.fake_redis)

    def enqueue(self, func, *args, **kwargs) -> Job:
        return self.queue.enqueue(func, *args, **kwargs)

    def get_status(self, job_id: str) -> JobStatus:
        job = Job.fetch(job_id, connection=self.fake_redis)
        return job.get_status()

    def get_result(self, job_id: str) -> Optional[Any]:
        job = Job.fetch(job_id, connection=self.fake_redis)
        return job.return_value()
