import os
import chainlit as cl
from dotenv import load_dotenv
from typing import Dict, Tuple

from langstream import debug
from streams.collection import chat_stream_factory, score_stream_factory, document_stream_factory

from store.document_store import DocumentStore
from utils.embeddings_handler import OpenAIGenerator
from store.database import ChromaDB

load_dotenv(dotenv_path="./.env")

DB_DIRECTORY = os.environ.get("DB_PATH", "./f-ai.db")
DB_COLLECTION = os.environ.get("DB_PLANNING_PERMISSION_COLLECTION_NAME", "planning_permission")
DOCUMENTS_TO_EMBED = os.environ.get("DOCUMENTS_TO_EMBED")

document_store = DocumentStore(
    db=ChromaDB(DB_DIRECTORY, DB_COLLECTION),
    embeddings_generator=OpenAIGenerator(),
)

def main(q: str):
    add_document, list_documents = *(lambda documents: (
        lambda document: (documents.append(document), document)[1], 
        lambda: [*documents]
    ))([]),
              
    document_stream, score_stream, chat_stream = (
        document_stream_factory(q, document_store, 10),
        score_stream_factory(q),
        chat_stream_factory(q)
    )

    return (
        debug(
            document_stream
            .map(add_document)
            .map(score_stream)
            .gather()
            .and_then(lambda scores: list(zip([*list_documents()], [s[0] for s in scores])))
            .and_then(lambda docs: sorted(docs[0], key=lambda x: x[1], reverse=True))
            .and_then(lambda docs: [i[0] for i in docs[0]][:4])
            .and_then(lambda docs: {"context": docs[0]})
            .and_then(chat_stream)
        )
    )(q)     

@cl.on_chat_start
async def start():
    if document_store.is_collection_empty():
        document_store.load_document(pathname=DOCUMENTS_TO_EMBED)

@cl.on_message
async def on_message(message: str):
    messages_map: Dict[str, Tuple[bool, cl.Message]] = {}

    async for output in main(message):
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