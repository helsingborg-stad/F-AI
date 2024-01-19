from config import settings


class Phrase:
    def __init__(self, mapping_by_language: dict[str, dict[str, str]], default_language: str):
        self.translations: dict[str, dict[str, str]] = mapping_by_language
        self.default_language: str = default_language
        self.current_language: str = default_language

    def set_language(self, language: str) -> None:
        self.current_language = language

    def __call__(self, key: str, default: str | None = None) -> str:
        if not isinstance(key, str):
            raise TypeError('Key must be a string')
        if default is not None and not isinstance(default, str):
            raise TypeError('Default value must be a string')

        lang: str = self.current_language if self.current_language in self.translations else self.default_language
        return self.translations.get(lang, {}).get(key, default if default is not None else key)


language_mappings = {
    'en': {'greeting': 'Hello'},
    'sv': {'greeting': 'Hej', 'logout_button_text': 'Logga ut', 'my_questions': 'Mina frågor',
           'submit_a_question': 'Ställ en fråga', 'submit_question': 'Ställ en fråga', 'questions': 'Frågor'},
}

phrase = Phrase(language_mappings, settings.DEFAULT_LANGUAGE)
