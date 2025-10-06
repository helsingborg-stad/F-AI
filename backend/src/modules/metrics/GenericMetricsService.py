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
        all_metrics = [metric for provider in self._providers for metric in await provider.get_metrics()]
        return self._serializer.serialize(all_metrics)
