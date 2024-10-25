import gettext
import os

from fai_backend.config import settings


class UnsupportedLanguageError(Exception):
    pass


class Phrase:
    def __init__(self, default_language: str = settings.DEFAULT_LANGUAGE) -> None:
        self.locale_path = os.path.join(os.path.dirname(__file__), 'locale')
        self.translation = None
        self.set_language(default_language)

    def set_language(self, selected_language: str) -> None:
        try:
            new_translation = gettext.translation(domain='messages', localedir=self.locale_path,
                                                  languages=[selected_language])
            new_translation.install()
            self.translation = new_translation
        except FileNotFoundError:
            if selected_language != settings.DEFAULT_LANGUAGE:
                self.set_language(settings.DEFAULT_LANGUAGE)
            else:
                raise UnsupportedLanguageError(f'Could not find locale for {selected_language}')

    def translate(self, key: str) -> str:
        if not self.translation:
            raise ValueError('Language not set. Call set_language() before calling translate()')

        return self.translation.gettext(key)


phrase_instance = Phrase()


def phrase(key: str, default: str | None = None, **kwargs) -> str:
    if not isinstance(key, str):
        raise TypeError('Key must be a string')
    if default is not None and not isinstance(default, str):
        raise TypeError('Default value must be a string')

    translated = phrase_instance.translate(key)
    if translated == key and default:
        translated = default

    return translated.format(**kwargs)


def set_language(language: str) -> None:
    phrase_instance.set_language(language)
