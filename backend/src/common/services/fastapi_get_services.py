from typing import Annotated

from src.common.services.models.Services import Services
from fastapi import Request, Depends


def get_services(request: Request) -> Services:
    services = request.app.state.services
    return services


ServicesDependency = Annotated[Services, Depends(get_services)]
