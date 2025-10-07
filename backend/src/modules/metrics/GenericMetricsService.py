from src.modules.metrics.models.Metric import Metric
from src.modules.metrics.protocols.IMetricsProvider import IMetricsProvider
from src.modules.metrics.protocols.IMetricsSerializer import IMetricsSerializer
from src.modules.metrics.protocols.IMetricsService import IMetricsService


class GenericMetricsService(IMetricsService):
    _providers: list[IMetricsProvider] = []

    def __init__(self, serializer: IMetricsSerializer):
        self._serializer = serializer

    def add_metrics_provider(self, provider: IMetricsProvider):
        self._providers.append(provider)

    async def get_serialized_metrics(self) -> str:
        all_metrics = [metric for provider in self._providers for metric in await self._try_get_metrics(provider)]
        return self._serializer.serialize(all_metrics)

    @staticmethod
    async def _try_get_metrics(provider: IMetricsProvider) -> list[Metric]:
        try:
            return await provider.get_metrics()
        except Exception as e:
            print(f"Error getting metrics from {provider}: {e}")
            return []
