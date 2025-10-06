from pydantic import BaseModel

from src.modules.metrics.models.MetricType import MetricType


class MetricValue(BaseModel):
    timestamp_s: int
    value: float | int
    attributes: dict[str, str]


class Metric(BaseModel):
    name: str
    help: str
    type: MetricType
    values: list[MetricValue]
