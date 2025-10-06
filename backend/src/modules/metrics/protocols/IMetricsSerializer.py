from typing import Protocol

from src.modules.metrics.models.Metric import Metric


class IMetricsSerializer(Protocol):
    def serialize(self, metrics: list[Metric]) -> str:
        raise NotImplementedError
