from typing import TypedDict

OpenAIStreamSettings = TypedDict('OpenAIStreamSettings', {
    'model': str,
    'temperature': float
})

SETTINGS_GPT_3_5 = OpenAIStreamSettings(model='gpt-3.5-turbo', temperature=0)
SETTINGS_GPT_3_5_16K = OpenAIStreamSettings(model='gpt-3.5-turbo-16k', temperature=0)
SETTINGS_GPT_4 = OpenAIStreamSettings(model='gpt-4', temperature=0)