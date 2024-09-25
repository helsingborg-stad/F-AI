import bson

from fai_backend.assistant.assistant import Assistant
from fai_backend.assistant.models import (
    AssistantContext,
    AssistantStreamConfig,
    AssistantStreamMessage,
    AssistantStreamPipelineDef,
    AssistantTemplate,
    AssistantTemplateMeta,
)
from fai_backend.assistant.protocol import IAssistantContextStore
from fai_backend.assistant.schema import TemplatePayload
from fai_backend.projects.service import ProjectService


class AssistantFactory:
    def __init__(self, assistant_templates: list[AssistantTemplate]):
        self.assistant_templates = assistant_templates

    def create_assistant(self, assistant_id) -> Assistant:
        template = next(a for a in self.assistant_templates if a.id == assistant_id)
        assistant = self.create_assistant_from_template(template)
        return assistant

    @staticmethod
    def create_assistant_from_template(template):
        return Assistant(template, InMemoryAssistantContextStore())


class InMemoryAssistantContextStore(IAssistantContextStore):
    def __init__(self):
        self.context = AssistantContext()

    def get_mutable(self) -> AssistantContext:
        return self.context


class AssistantTemplateStore:
    service: 'ProjectService'

    def __init__(self, project_service: 'ProjectService'):
        self.service = project_service

    async def get_assistant_template(self, project_id: str, assistant_id: str) -> AssistantTemplate | None:
        project = await self.service.read_project(project_id)
        return self._assistant_by_id(project.assistants, assistant_id) if project else None

    async def list_assistant_templates(self, project_id: str) -> list[AssistantTemplate] | None:
        project = await self.service.read_project(project_id)
        return project.assistants if project else None

    async def put_assistant_template(self, project_id: str, template: AssistantTemplate) -> AssistantTemplate | None:
        project = await self.service.read_project(project_id)
        template.id = (bson.ObjectId()).__str__() if template.id == '' else template.id
        project.assistants = [a for a in project.assistants if a.id != template.id]
        project.assistants.append(template)
        updated_project = await self.service.update_project(project_id, project)
        return await self.get_assistant_template(project_id, template.id) if updated_project else None

    async def delete_assistant_template(self, project_id: str, assistant_id: str) -> AssistantTemplate | None:
        project = await self.service.read_project(project_id)
        assistant = self._assistant_by_id(project.assistants, assistant_id)
        project.assistants = [a for a in project.assistants if a.id != assistant_id]
        await self.service.update_project(project_id, project)
        return assistant if assistant else None

    @staticmethod
    def _assistant_by_id(assistants: list[AssistantTemplate], assistant_id: str) -> AssistantTemplate | None:
        return next((assistant for assistant in assistants if assistant.id == assistant_id), None)


class TemplatePayloadAdapter:
    @staticmethod
    def to_template_payload(template: AssistantTemplate) -> TemplatePayload:
        def basic_stream_adapter():
            return TemplatePayload(
                id=template.id,
                name=template.meta.name,
                description=template.meta.description,
                sample_questions=template.meta.sample_questions,
                model=template.streams[0].settings['model'] or '',
                temperature=template.streams[0].settings['temperature'] or 1.0,
                instructions=template.streams[0].messages[0].content or '',
                files_collection_id=template.files_collection_id,
            )

        def rag_stream_adapter():
            return TemplatePayload(
                id=template.id,
                name=template.meta.name,
                description=template.meta.description,
                sample_questions=template.meta.sample_questions,
                model=template.streams[1].settings['model'] or '',
                temperature=template.streams[1].settings['temperature'] or 1.0,
                instructions=template.streams[1].messages[0].content or '',
                files_collection_id=template.files_collection_id,
            )

        return basic_stream_adapter() if len(template.streams) == 1 else rag_stream_adapter()

    @staticmethod
    def from_template_payload(payload: TemplatePayload) -> AssistantTemplate:
        def basic_stream():
            return [
                AssistantStreamConfig(
                    provider='openai',
                    settings={
                        'model': payload.model,
                        'temperature': payload.temperature,
                    },
                    messages=[
                        AssistantStreamMessage(
                            role='system',
                            content=payload.instructions
                        ),
                        AssistantStreamMessage(
                            role='user',
                            content='{query}'
                        ),
                    ]
                )
            ]

        def rag_stream():
            return [
                AssistantStreamPipelineDef(
                    pipeline='rag_scoring'
                ),
                AssistantStreamConfig(
                    provider='openai',
                    settings={
                        'model': payload.model,
                        'temperature': payload.temperature,
                    },
                    messages=[
                        AssistantStreamMessage(
                            role='system',
                            content=payload.instructions
                        ),
                        AssistantStreamMessage(
                            role='user',
                            content='{query}'
                        ),
                        AssistantStreamMessage(
                            role='user',
                            content='Here are the results of the search:\n\n {rag_output}'
                        ),
                    ]
                )
            ]

        return AssistantTemplate(
            id=payload.id,
            meta=AssistantTemplateMeta(
                name=payload.name,
                description=payload.description or '',
                sample_questions=filter(
                    lambda q: q and q != '',
                    list(payload.sample_questions)) if payload.sample_questions and len(
                    payload.sample_questions) > 0 else []
            ),
            files_collection_id=payload.files_collection_id,
            streams=basic_stream() if payload.files_collection_id is None else rag_stream()
        )
