from redis import Redis
from rq import Worker, Queue, Connection

from worker_src.helpers import config


redis_conn = Redis(host=config["REDIS_HOST"],
                   port=config["REDIS_PORT"],
                   password=config["REDIS_PASSWORD"],
                   username=config["REDIS_USERNAME"],
                   db=0)
listen = ["default"]


def run_worker() -> None:
    with Connection(redis_conn):
        w = Worker(map(Queue, listen))
        w.work(logging_level=config["REDIS_LOG_LEVEL"])
