from src.modules.settings.protocols.ISettingsService import ISettingsService


async def setup_default_settings(settings_service: ISettingsService):
    await settings_service.set_setting('jwt.user_secret', 'CHANGE THIS')
