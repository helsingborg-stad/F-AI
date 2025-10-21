from src.modules.metrics.GenericMetricsService import GenericMetricsService
from src.modules.metrics.OpenMetricsSerializer import OpenMetricsSerializer
from src.modules.metrics.protocols.IMetricsService import IMetricsService


class MetricsServiceFactory:
    def get(self) -> IMetricsService:
        return GenericMetricsService(serializer=OpenMetricsSerializer())
