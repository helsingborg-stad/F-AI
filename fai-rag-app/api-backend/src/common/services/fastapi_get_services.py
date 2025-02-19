from src.common.services.models.Services import Services
from fastapi import Request


def get_services(request: Request) -> Services:
    services = request.app.state.services
    return services
