from src.modules.metrics.OpenMetricsSerializer import OpenMetricsSerializer
from src.modules.metrics.models.Metric import Metric, MetricValue


class TestOpenMetricsSerializer:
    @staticmethod
    def test_empty():
        serializer = OpenMetricsSerializer()
        result = serializer.serialize([])

        assert result == '# EOF\n'

    @staticmethod
    def test_basic():
        serializer = OpenMetricsSerializer()
        result = serializer.serialize([
            Metric(
                name='requests_total',
                help='My test metric',
                type='counter',
                values=[
                    MetricValue(timestamp_s=12345, value=5, attributes={'method': 'GET'})
                ]
            )
        ])

        assert result == ('# HELP requests_total My test metric\n'
                          '# TYPE requests_total counter\n'
                          'requests_total{method="GET"} 5 12345\n'
                          '# EOF\n')

    @staticmethod
    def test_multiple_values():
        serializer = OpenMetricsSerializer()
        result = serializer.serialize([
            Metric(
                name='requests_total',
                help='My test metric',
                type='counter',
                values=[
                    MetricValue(timestamp_s=12345, value=5, attributes={'method': 'GET', 'endpoint': '/api/v1/test'}),
                    MetricValue(timestamp_s=12346, value=10, attributes={'method': 'POST', 'endpoint': '/api/v1/test'})
                ]
            )
        ])

        assert result == ('# HELP requests_total My test metric\n'
                          '# TYPE requests_total counter\n'
                          'requests_total{method="GET",endpoint="/api/v1/test"} 5 12345\n'
                          'requests_total{method="POST",endpoint="/api/v1/test"} 10 12346\n'
                          '# EOF\n')

    @staticmethod
    def test_multiple_metrics():
        serializer = OpenMetricsSerializer()
        result = serializer.serialize([
            Metric(
                name='requests_total',
                help='My test metric',
                type='counter',
                values=[
                    MetricValue(timestamp_s=12345, value=5, attributes={'method': 'GET', 'endpoint': '/api/v1/test'}),
                    MetricValue(timestamp_s=12346, value=10, attributes={'method': 'POST', 'endpoint': '/api/v1/test'})
                ]
            ),
            Metric(
                name='users_logged_in_count',
                help='Amount of logged in users',
                type='gauge',
                values=[
                    MetricValue(timestamp_s=12345, value=50, attributes={}),
                ]
            )
        ])

        assert result == ('# HELP requests_total My test metric\n'
                          '# TYPE requests_total counter\n'
                          'requests_total{method="GET",endpoint="/api/v1/test"} 5 12345\n'
                          'requests_total{method="POST",endpoint="/api/v1/test"} 10 12346\n'
                          '# HELP users_logged_in_count Amount of logged in users\n'
                          '# TYPE users_logged_in_count gauge\n'
                          'users_logged_in_count 50 12345\n'
                          '# EOF\n')

    @staticmethod
    def test_float_value():
        serializer = OpenMetricsSerializer()
        result = serializer.serialize([
            Metric(
                name='cpu_used',
                help='Processor utilization',
                type='gauge',
                values=[
                    MetricValue(timestamp_s=12345, value=42.069, attributes={}),
                ]
            )
        ])

        assert result == ('# HELP cpu_used Processor utilization\n'
                          '# TYPE cpu_used gauge\n'
                          'cpu_used 42.069 12345\n'
                          '# EOF\n')
