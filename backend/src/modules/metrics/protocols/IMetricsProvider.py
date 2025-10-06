from typing import Protocol

from src.modules.metrics.models.Metric import Metric


class IMetricsProvider(Protocol):
    async def get_metrics(self) -> list[Metric]:
        raise NotImplementedError
