from typing import Iterator, Tuple

from src.modules.settings.models.Setting import Setting


class SettingKeyMeta(type):
    def __iter__(cls) -> Iterator[Tuple[str, Setting]]:
        for prop_name, value in vars(cls).items():
            if not prop_name.startswith('_') and isinstance(value, Setting):
                yield prop_name, value


class SettingKey(metaclass=SettingKeyMeta):
    FIXED_OTP = Setting('login.fixed_otp', '1234')
    OTP_EXPIRE_SECONDS = Setting('login.otp_expire_seconds', 900)
    JWT_USER_SECRET = Setting('jwt.user_secret', 'CHANGE THIS')
    JWT_EXPIRE_MINUTES = Setting('jwt.expire_minutes', 600)
    REFRESH_TOKEN_EXPIRE_MINUTES = Setting('refresh_token.expire_minutes', 30 * 24 * 60) # 30 days

    BREVO_URL = Setting('brevo.url', 'https://api.brevo.com/v3/smtp/email')
    BREVO_API_KEY = Setting('brevo.api_key', '')
    BREVO_SENDER_NAME = Setting('brevo.sender_name', 'Folkets AI Helsingborg')
    BREVO_SENDER_EMAIL = Setting('brevo.sender_email', 'no-reply@folkets-ai.helsingborg.io')

    OPENAI_API_KEY = Setting('openai.api_key', '')
    ANTHROPIC_API_KEY = Setting('anthropic.api_key', '')
    MISTRAL_API_KEY = Setting('mistral.api_key', '')


if __name__ == '__main__':
    print(SettingKey.JWT_USER_SECRET)
    print(SettingKey.JWT_USER_SECRET.default)

    # Example of iterating through the settings
    print("\nAll settings:")
    for name, setting in SettingKey:
        print(f"{name}: {setting.key} = {setting.default}")
