from src.modules.metrics.protocols.IMetricsProvider import IMetricsProvider


class IMetricsService:
    def add_metrics_provider(self, provider: IMetricsProvider):
        raise NotImplementedError

    async def get_serialized_metrics(self) -> str:
        raise NotImplementedError
