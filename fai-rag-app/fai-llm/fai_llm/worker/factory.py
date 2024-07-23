from fai_llm.worker.protocol import IWorkerFactory
from fai_llm.worker.service import MPWorkerService


class DefaultWorkerFactory(IWorkerFactory):
    def create(self):
        return MPWorkerService()
