from typing import TypedDict

OpenAIStreamSettings = TypedDict('OpenAIStreamSettings', {
    'model': str,
    'temperature': float
})

default_settings = OpenAIStreamSettings(model='gpt-3.5-turbo', temperature=0.5)