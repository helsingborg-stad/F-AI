from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.settings.models.SettingValue import SettingValue, SettingsDict
from src.modules.settings.settings import SettingKey

settings_router = APIRouter(
    prefix='/settings',
    tags=['Settings']
)

auth = AuthRouterDecorator(settings_router)


class GetSettingsResponse(BaseModel):
    settings: SettingsDict = Field(
        examples=[{SettingKey.JWT_USER_SECRET: "my_jwt_secret", SettingKey.JWT_EXPIRE_SECONDS: 900}])


@auth.get(
    '',
    ['settings.read'],
    response_model=GetSettingsResponse,
)
async def get_settings(services: ServicesDependency):
    settings = await services.settings_service.get_settings()
    return GetSettingsResponse(settings=settings)


class GetSettingResponse(BaseModel):
    value: SettingValue | None


@auth.get(
    '/{key}',
    ['settings.read'],
    response_model=GetSettingResponse,
)
async def get_setting(key: str, services: ServicesDependency):
    value = await services.settings_service.get_setting(key)
    return GetSettingResponse(value=value)


class SetSettingRequest(BaseModel):
    key: str
    value: SettingValue


@auth.post(
    '/{key}',
    ['settings.write']
)
async def set_setting(body: SetSettingRequest, services: ServicesDependency):
    await services.settings_service.set_setting(key=body.key, value=body.value)


class PatchSettingsRequest(BaseModel):
    settings: SettingsDict = Field(
        examples=[{SettingKey.JWT_USER_SECRET: "asdfasdf", SettingKey.JWT_EXPIRE_SECONDS: 900}])


@auth.patch(
    '',
    ['settings.write']
)
async def patch_settings(body: PatchSettingsRequest, services: ServicesDependency):
    await services.settings_service.patch_settings(patch=body.settings)
