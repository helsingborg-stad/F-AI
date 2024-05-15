import json

from langstream import Stream, join_final_output, as_async_generator
from langstream.contrib import OpenAIChatStream, OpenAIChatMessage, OpenAIChatDelta

from fai_backend.chat.stream import create_chat_stream_from_prompt
from fai_backend.chat.template import CHAT_PROMPT_TEMPLATE_ARGS, SCORING_PROMPT_TEMPLATE_ARGS
from fai_backend.vector.service import VectorService
from fai_backend.vector.factory import vector_db

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
    add_document, list_documents = (lambda documents: (
        lambda document: (documents.append(document), document)[1],
        lambda: [*documents]
    ))([])

    chat_stream, _ = create_chat_stream_from_prompt(CHAT_PROMPT_TEMPLATE_ARGS)
    scoring_stream, _ = create_chat_stream_from_prompt(SCORING_PROMPT_TEMPLATE_ARGS)
    vector_service = VectorService(vector_db=vector_db)

    def append_score_to_documents(scores):
        return zip(list_documents(), [s[0] for s in scores])

    def sort_and_slice_documents(scored_documents, slice_size: int):
        first_element = list(scored_documents)[0]
        sorted_scores = sorted(first_element, key=lambda x: x[1], reverse=True)
        return sorted_scores[:slice_size]

    def create_query_document_pair(query, document):
        return {"query": query, "document": document}

    vector_db_query_result = await query_vector(
        vector_service=vector_service,
        collection_name=collection_name,
        query=question,
    )

    scoring_stream = scoring_stream.map(
        lambda delta: json.loads(delta.content)['score']
        if delta.role == "function" and delta.name == "score_document"
        else 0
    )

    def stream(query):
        try:
            return (
                vector_db_query_result
                .map(add_document)
                .map(lambda document: create_query_document_pair(query, document))
                .map(scoring_stream)
                .gather()
                .and_then(append_score_to_documents)
                .and_then(lambda scored_documents: sort_and_slice_documents(scored_documents, 6))
                .and_then(lambda results: {"query": query, "results": results[0]})
                .and_then(chat_stream)
                .map(lambda delta: delta.content)
            )(query)
        except Exception as e:
            print(f"Error processing query: {e}", {str(e)})
            raise e

    try:
        return await join_final_output(stream(question))
    except Exception as e:
        print(f"Error joining final output '{question}': {str(e)}")
        raise e
