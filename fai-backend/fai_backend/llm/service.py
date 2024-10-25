from langstream import Stream, join_final_output, as_async_generator
from langstream.contrib import OpenAIChatStream, OpenAIChatMessage, OpenAIChatDelta

from fai_backend.projects.dependencies import get_project_service

SYSTEM_TEMPLATE = "You are a helpful AI assistant that helps people with answering questions about planning "
"permission.<br> If you can't find the answer in the search result below, just say (in Swedish) "
"\"Tyvärr kan jag inte svara på det.\" Don't try to make up an answer.<br> If the "
"question is not related to the context, politely respond that you are tuned to only "
"answer questions that are related to the context.<br> The questions are going to be "
"asked in Swedish. Your response must always be in Swedish."


async def query_vector(vector_service, collection_name, query, n_results=10):
    vector_result = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=[query],
        n_results=n_results,
    )

    documents = vector_result['documents'][0] if 'documents' in vector_result and vector_result['documents'] else []

    return Stream[None, str](
        "QueryVectorStream",
        lambda _: as_async_generator(*documents)
    )


async def ask_llm_question(question: str):
    llm_stream: Stream[str, str] = OpenAIChatStream[str, OpenAIChatDelta](
        "AskLLMStream",
        lambda user_question: [
            OpenAIChatMessage(
                role="system",
                content=SYSTEM_TEMPLATE
            ),
            OpenAIChatMessage(
                role="user",
                content=f"{user_question}",
            ),
        ],
        model="gpt-4",
        temperature=0,
    ).map(lambda delta: delta.content)

    return await join_final_output(llm_stream(question))


async def ask_llm_raq_question(question: str, collection_name: str):
    from fai_backend.assistant.assistant import Assistant
    from fai_backend.assistant.service import InMemoryAssistantContextStore
    projects = await get_project_service().read_projects()
    template = next(a for a in projects[0].assistants if a.id == '_qaf')
    template.files_collection_id = collection_name
    context = InMemoryAssistantContextStore()
    assistant = Assistant(template, context)
    stream = await assistant.create_stream()
    return await join_final_output(stream(question))
