import os
import json

from typing import Dict, Optional
from dotenv import load_dotenv
from langstream import debug, Stream
import chainlit as cl

from planning_permission.store.document_store import DocumentStore
from planning_permission.utils.embeddings_handler import OpenAIGenerator
from planning_permission.store.database import ChromaDB

from numpy import add
from typing import Dict, Callable, Optional
from langstream import debug, Stream
from langstream.contrib import OpenAIChatDelta

from planning_permission.chat.stream import create_chat_stream_from_prompt
from planning_permission.chat.prompt import ChatPrompt
from planning_permission.chat.templates import CHAT_PROMPT_TEMPLATE_ARGS, SCORING_PROMPT_TEMPLATE_ARGS


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

DEBUG_STREAM = os.environ.get("DEBUG_STREAM", False)

def use_chat_stream(query: str, debug_fn: Optional[Callable] = None )-> tuple[Stream[str, OpenAIChatDelta], Dict[str, ChatPrompt]]:
    add_document, list_documents = (lambda documents: (
        lambda document: (documents.append(document), document)[1],
        lambda: [*documents]
    ))([])
    
    chat_stream, chat_prompt = create_chat_stream_from_prompt(CHAT_PROMPT_TEMPLATE_ARGS)
    scoring_stream, scoring_prompt = create_chat_stream_from_prompt(SCORING_PROMPT_TEMPLATE_ARGS)
    
    scoring_stream = scoring_stream.map(
        lambda delta: (lambda num: num)(json.loads(delta.content)['score'])
        if delta.role == "function" and delta.name == "score_document"
        else 0
    )

    stream = (
        Stream[str, str](
            "RetrieveDocumentsStream",
            lambda query: document_store.query(query=query, n_results=10)
        )
        .map(add_document)
        .map(lambda document: {"query": query, "document": document})
        .map(scoring_stream)
        .gather()
        .and_then(lambda scores: zip(list_documents(), [s[0] for s in scores]))
        .and_then(lambda scored: sorted(list(scored)[0], key=lambda x: x[1], reverse=True)[:4])
        .and_then(lambda results: {"query": query, "results": results[0]})
        .and_then(chat_stream)
    )

    return (
        (debug_fn or (lambda x: x))(stream), 
        {
            chat_prompt.name: chat_prompt,
            scoring_prompt.name: scoring_prompt,
        }
    )

@cl.on_message
async def on_message(message: str):
    stream, prompts = use_chat_stream(message, debug if DEBUG_STREAM else None)
   
    cl_messages_map: Dict[str, cl.Message] = {}
    
    async for output in stream(message):
        if "@" in output.stream and not output.final:
            continue

        if output.stream in cl_messages_map:
            cl_message = cl_messages_map[output.stream]
            await cl_message.stream_token(
                output.data.content if hasattr(output.data, "content") else ""
            )
        else:
            if hasattr(output.data, "content"):
                cl_messages_map[output.stream] = cl.Message(
                    author=output.stream,
                    content= output.data.content,
                    indent=0 if output.final else 1,
                    prompt=prompts[output.stream].to_prompt() if output.stream in prompts else None
                )

    for cl_message in cl_messages_map.values():
        if cl_message.prompt:
            cl_message.prompt.completion = cl_message.content or ""
        await cl_message.send()
 
            

