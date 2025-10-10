from fastapi import APIRouter, Response

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator

metrics_router = APIRouter(
    prefix='/metrics',
    tags=['Metrics']
)

auth = AuthRouterDecorator(metrics_router)


class OpenMetricsResponse(Response):
    media_type = "application/openmetrics-text; version=1.0.0; charset=utf-8"


@auth.get('', ['metrics.read'], additional_responses={
    200: {
        "content": {
            "application/json": None,
            "application/openmetrics-text; version=1.0.0; charset=utf-8": {
                "example": "# HELP api_requests_total Total number of API requests per endpoint\n# TYPE api_requests_total counter\napi_requests_total{endpoint=\"/metrics\"} 42 12345\n# EOF\n"
            }
        }
    }
})
async def get_metrics(services: ServicesDependency):
    result = await services.metrics_service.get_serialized_metrics()
    return OpenMetricsResponse(result)
