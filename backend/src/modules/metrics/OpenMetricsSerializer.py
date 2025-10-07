from src.modules.metrics.models.Metric import Metric
from src.modules.metrics.protocols.IMetricsSerializer import IMetricsSerializer


class OpenMetricsSerializer(IMetricsSerializer):
    def serialize(self, metrics: list[Metric]) -> str:
        if len(metrics) == 0:
            return "# EOF\n"
        outputs = [
            OpenMetricsSerializer._metric_to_string(metric)
            for metric in metrics
        ]
        return "\n".join(outputs) + "\n# EOF\n"

    @staticmethod
    def _metric_to_string(metric: Metric) -> str:
        value_strings = "\n".join([
            f"{metric.name}{OpenMetricsSerializer._attributes_to_string(v.attributes)} {v.value} {v.timestamp_s}"
            for v in metric.values
        ])
        return (f"# HELP {metric.name} {metric.help}\n"
                f"# TYPE {metric.name} {metric.type}\n"
                f"{value_strings}")

    @staticmethod
    def _attributes_to_string(attributes: dict[str, str]) -> str:
        if len(attributes) == 0:
            return ""
        return "{" + ",".join([f"{k}=\"{v}\"" for k, v in attributes.items()]) + "}"
