import os

from src.modules.models.models.Model import Model
from src.modules.models.protocols.IModelService import IModelService


async def setup_default_models(model_service: IModelService):
    existing = await model_service.get_available_models(as_uid=os.environ['SETUP_ADMIN'])

    if len(existing) > 0:
        return

    await model_service.set_available_models(models=[
        Model(
            key='openai/o3-mini',
            provider='OpenAI',
            display_name='ChatGPT o3-mini',
            description='A small reasoning model, providing high intelligence at the a smaller cost and latency',
            meta={
                'primaryColor': '#8bd0c6',
                'context_window': 200000,
                'max_output_tokens': 100000,
                'supports_imagegen': False,
                'supports_function_calling': True
            }
        ),
        Model(
            key='openai/gpt-4o',
            provider='OpenAI',
            display_name='ChatGPT 4o',
            description='Fast, intelligent, flexible GPT model',
            meta={
                'primaryColor': '#8bd0c6',
                'context_window': 128000,
                'max_output_tokens': 16384,
                'supports_imagegen': True,
                'supports_function_calling': True,
            }
        ),
        Model(
            key='openai/gpt-3.5-turbo',
            provider='OpenAI',
            display_name='ChatGPT 3.5 Turbo',
            description='Fast and efficient model for standard tasks',
            meta={
                'primaryColor': '#8bd0c6',
                'context_window': 16385,
                'max_output_tokens': 4096,
                'supports_imagegen': False,
                'supports_function_calling': True,
                'supports_json_mode': True
            }
        ),

        Model(
            key='anthropic/claude-3-7-sonnet-latest',
            provider='Anthropic',
            display_name='Claude 3.7 Sonnet',
            description='Balanced model with strong reasoning and creative capabilities',
            meta={
                'primaryColor': '#b18be0',
                'context_window': 200000,
                'max_output_tokens': 8192,
                'supports_imagegen': True,
                'supports_function_calling': True,
                'training_cutoff': '2024-04'
            }
        ),

        Model(
            key='mistral/mistral-large-latest',
            provider='Mistral',
            display_name='Mistral Large',
            description='Top-tier reasoning model with native function calling',
            meta={
                'primaryColor': '#f0d27a',
                'context_window': 128000,
                'max_output_tokens': 8192,
                'supports_imagegen': False,
                'supports_function_calling': True,
                'supports_json_mode': True,
                'training_cutoff': '2024-07'
            }
        )
    ])
