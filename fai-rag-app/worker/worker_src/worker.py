from redis import Redis
from rq import Worker, Queue, Connection

redis_conn = Redis(host='redis', port=6379, db=0)
listen = ['default']


def run_worker() -> None:
    print("WORKER STARTED")
    with Connection(redis_conn):
        w = Worker(map(Queue, listen))
        w.work()
    print("WORKER STOPPED")
