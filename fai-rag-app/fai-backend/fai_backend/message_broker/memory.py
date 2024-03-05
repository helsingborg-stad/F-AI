import fakeredis
from rq import Queue, Worker, Connection
from rq.job import Job

from fai_backend.message_broker.interface import IMessageQueue


class MemoryQueue(IMessageQueue):
    def __init__(self):
        self.fake_redis = fakeredis.FakeStrictRedis()
        self.queue = Queue(is_async=False, connection=self.fake_redis)

    def enqueue(self, func, *args, **kwargs):
        job = self.queue.enqueue(func, *args, **kwargs)
        return job.get_id()

    def get_status(self, job_id):
        job = Job.fetch(job_id, connection=self.fake_redis)
        return job.get_status()

    def get_result(self, job_id):
        job = Job.fetch(job_id, connection=self.fake_redis)
        return job.return_value() if job.is_finished else None
