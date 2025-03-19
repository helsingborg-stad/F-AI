from fastapi import APIRouter
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.settings.models.SettingValue import SettingValue

settings_router = APIRouter(
    prefix='/settings',
    tags=['Settings']
)

auth = AuthRouterDecorator(settings_router)


class GetSettingsResponse(BaseModel):
    settings: dict[str, SettingValue]


@auth.get(
    '/settings',
    ['settings.read']
)
async def get_settings(services: ServicesDependency):
    settings = await services.settings_service.get_settings()
    return GetSettingsResponse(settings=settings)


class GetSettingResponse(BaseModel):
    value: SettingValue | None


@auth.get(
    'settings/{key}',
    ['settings.read']
)
async def get_setting(key: str, services: ServicesDependency):
    value = await services.settings_service.get_setting(key)
    return GetSettingResponse(value=value)


class SetSettingRequest(BaseModel):
    key: str
    value: SettingValue


@auth.post(
    'settings/{key}',
    ['settings.write']
)
async def set_setting(body: SetSettingRequest, services: ServicesDependency):
    await services.settings_service.set_setting(key=body.key, value=body.value)
