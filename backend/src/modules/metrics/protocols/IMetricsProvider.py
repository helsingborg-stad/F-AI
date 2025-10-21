from typing import Protocol, runtime_checkable

from src.modules.metrics.models.Metric import Metric

@runtime_checkable
class IMetricsProvider(Protocol):
    async def get_metrics(self) -> list[Metric]:
        raise NotImplementedError
