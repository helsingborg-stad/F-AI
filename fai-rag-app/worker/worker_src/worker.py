from redis import Redis
from rq import Worker, Queue, Connection

redis_conn = Redis(host='redis', port=6379, db=0)
listen = ['default']


def run_worker() -> None:
    with Connection(redis_conn):
        w = Worker(map(Queue, listen))
        w.work(logging_level="DEBUG")
