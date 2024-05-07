import gettext
import os

from fai_backend.config import settings


class Phrase:
    _instance = None

    def __new__(cls, selected_language: str = 'en', **kwargs):
        if not cls._instance:
            cls._instance = super(Phrase, cls).__new__(cls)
            cls._instance._initialize(selected_language)
        return cls._instance

    def _initialize(self, selected_language: str) -> None:
        try:
            locale_path = os.path.join(os.path.dirname(__file__), 'locale')
            self.translation = gettext.translation(domain='messages', localedir=locale_path,
                                                   languages=[selected_language])
        except FileNotFoundError:
            self.translation = gettext.NullTranslations()
        self.translation.install()

    def translate(self, key: str) -> str:
        return self.translation.gettext(key)


def translate_phrase(key: str, default: str = None, **kwargs) -> str:
    translated = Phrase(settings.DEFAULT_LANGUAGE).translate(key)
    if translated == key and default:
        translated = default

    return translated.format(**kwargs)


phrase = translate_phrase
