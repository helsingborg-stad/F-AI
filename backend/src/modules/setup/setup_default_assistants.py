import os

from src.modules.assistants.protocols.IAssistantService import IAssistantService


async def setup_default_assistants(assistant_service: IAssistantService):
    uid = os.environ['SETUP_ADMIN']
    existing = await assistant_service.get_available_assistants(as_uid=uid)

    if len(existing) > 0:
        return

    aid = await assistant_service.create_assistant(as_uid=uid)
    await assistant_service.update_assistant(
        as_uid=uid,
        assistant_id=aid,
        is_public=True,
        model='openai:gpt-4o',
        name='Vanilla ChatGPT',
        description='OpenAI ChatGPT 4o with no additional settings.'
    )

    aid = await assistant_service.create_assistant(as_uid=uid)
    await assistant_service.update_assistant(
        as_uid=uid,
        assistant_id=aid,
        is_public=True,
        model='anthropic:claude-3-7-sonnet-latest',
        name='Vanilla Claude',
        description='Anthropic Claude 3.7 Sonnet with no additional settings.'
    )

    aid = await assistant_service.create_assistant(as_uid=uid)
    await assistant_service.update_assistant(
        as_uid=uid,
        assistant_id=aid,
        is_public=True,
        model='mistral:mistral-large-latest',
        name='Vanilla Mistral',
        description='Mistral Large with no additional settings.'
    )
