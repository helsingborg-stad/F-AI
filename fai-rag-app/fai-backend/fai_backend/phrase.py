import gettext
import os
from typing import Any

from fai_backend.config import settings


class Phrase:
    _instance = None

    def __new__(cls, selected_language: str = 'sv', **kwargs):
        if not cls._instance:
            cls._instance = super(Phrase, cls).__new__(cls)
            cls._instance._initialize(selected_language)
        return cls._instance

    def _initialize(self, selected_language: str) -> None:
        locale_path = os.path.join(os.path.dirname(__file__), 'locale')
        self.translation = gettext.translation('messages', locale_path, languages=[selected_language])
        self.translation.install()

    def translate(self, key: str) -> str:
        return self.translation.gettext(key)


def translate_phrase(key: str, default: Any) -> str:
    return Phrase(settings.DEFAULT_LANGUAGE).translate(key)


phrase = translate_phrase
