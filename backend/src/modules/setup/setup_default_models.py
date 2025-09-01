import os

from src.modules.models.models.Model import Model
from src.modules.models.protocols.IModelService import IModelService


async def setup_default_models(model_service: IModelService):
    existing = await model_service.get_available_models(as_uid=os.environ['SETUP_ADMIN'])

    if len(existing) > 0:
        return

    await model_service.set_available_models(models=[
        Model(key='openai/o3-mini', provider='OpenAI', display_name='ChatGPT o3-mini', description=''),
        Model(key='openai/gpt-4o', provider='OpenAI', display_name='ChatGPT 4o', description=''),
        Model(key='openai/gpt-3.5-turbo', provider='OpenAI', display_name='ChatGPT 3.5 Turbo', description=''),

        Model(key='anthropic/claude-3-7-sonnet-latest', provider='Anthropic', display_name='Claude 3.7 Sonnet',
              description=''),

        Model(key='mistral/mistral-large-latest', provider='Mistral', display_name='Mistral Large', description='')
    ])
