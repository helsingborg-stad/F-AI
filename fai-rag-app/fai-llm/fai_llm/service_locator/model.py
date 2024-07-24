from dataclasses import dataclass

from fai_llm.app_life.service import AppLifeService
from fai_llm.log.service import ScopeableLogger
from fai_llm.worker.protocol import IWorkerService


@dataclass
class Services:
    main_logger: ScopeableLogger = None
    app_life: AppLifeService = None
    worker_service: IWorkerService = None
