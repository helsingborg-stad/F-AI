import os
from typing import Dict, Tuple, List
from dotenv import load_dotenv

from langstream import debug, Stream
import chainlit as cl

from planning_permission.streams.collection import get_scoring_stream, get_query_openai
from planning_permission.store.document_store import DocumentStore
from planning_permission.utils.embeddings_handler import OpenAIGenerator
from planning_permission.store.database import ChromaDB

load_dotenv(dotenv_path="./.env")
DB_DIRECTORY = os.environ.get("DB_PATH", "./f-ai.db")
DB_COLLECTION = os.environ.get("DB_PLANNING_PERMISSION_COLLECTION_NAME", "planning_permission")
DOCUMENTS_TO_EMBED = os.environ.get("DOCUMENTS_TO_EMBED")

document_store = DocumentStore(
    db=ChromaDB(DB_DIRECTORY, DB_COLLECTION),
    embeddings_generator=OpenAIGenerator(),
)

# Populate database with document embeddings if collection empty
if document_store.is_collection_empty():
    document_store.load_document(pathname=DOCUMENTS_TO_EMBED)


def stream_with_scoring(query):
    add_document, list_documents = (lambda documents: (
        lambda document: (documents.append(document), document)[1],
        lambda: [*documents]
    ))([])

    scoring_stream = get_scoring_stream(query)
    query_openai = get_query_openai(query)

    return (
        debug(
            Stream[str, str](
                "RetrieveDocumentsStream",
                lambda query: document_store.query(query=query, n_results=10)
            )
            .map(add_document)
            .map(scoring_stream)
            .gather()
            .and_then(lambda scores: zip(list_documents(), [s[0] for s in scores]))
            .and_then(lambda scored: sorted(list(scored)[0], key=lambda x: x[1], reverse=True)[:4])
            .and_then(query_openai)
        )
    )(query)


@cl.on_message
async def on_message(message: str):
    messages_map: Dict[str, Tuple[bool, cl.Message]] = {}

    async for output in stream_with_scoring(message):
        if "@" in output.stream and not output.final:
            continue
        if output.stream in messages_map:
            sent, cl_message = messages_map[output.stream]
            if not sent:
                await cl_message.send()
                messages_map[output.stream] = (False, cl_message)
            await cl_message.stream_token(output.data.content)
        else:
            if hasattr(output.data, "content"):
                messages_map[output.stream] = (
                    True,
                    cl.Message(
                        author=output.stream,
                        content=output.data.content,
                        indent=0 if output.final else 1,
                    ),
                )
