import gettext
import os

from fai_backend.config import settings


class Phrase:
    def __init__(self) -> None:
        self.locale_path = os.path.join(os.path.dirname(__file__), 'locale')
        self.current_language = 'sv'
        self.translation = None
        self.set_language(self.current_language)

    def set_language(self, selected_language='sv') -> None:
        try:
            new_translation = gettext.translation(domain='messages', localedir=self.locale_path,
                                                  languages=[selected_language])
            new_translation.install()
            self.current_language = selected_language
            self.translation = new_translation
        except FileNotFoundError:
            if self.current_language != 'sv':
                self.set_language('sv')

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
    try:
        phrase_instance.set_language(language)
    except ValueError as _:
        phrase_instance.set_language('sv')


set_language(settings.DEFAULT_LANGUAGE)
