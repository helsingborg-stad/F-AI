import dataclasses
import os
from typing import List, Callable, Any

from fai_backend.chat.prompt import UserChatPrompt, SystemChatPrompt, MessageChatPrompt


@dataclasses.dataclass
class PromptTemplate:
    name: str
    messages: List[MessageChatPrompt]

    # Takes the input T from a Stream[T,U] and returns a dict of replacement variables
    input_map_fn: Callable[[Any], dict[str, str]]

    settings: dict[str, Any]


scoringPromptTemplate = PromptTemplate(
    name="ScoringStream",
    messages=[
        SystemChatPrompt(
            "You are a scoring systems that classifies documents from 0-100 based on how well they answer a query."),
        UserChatPrompt("Query: {query}\n\nDocument: {document}"),
    ],
    input_map_fn=lambda input: {**(input)},
    settings={
        "model": os.environ.get("SCORING_MODEL", "gpt-3.5-turbo"),
        "temperature": 0,
        "functions": [
            {
                "name": "score_document",
                "description": "Scores the previous document according to the user query\n\n    Parameters\n    ----------\n    score\n        A number from 0-100 scoring how well does the document matches the query. The higher the score, the better match for the query\n    ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                        }
                    },
                    "required": ["score"],
                }
            }
        ],
        "function_call": {"name": "score_document"},
    }
)

CHAT_PROMPT_TEMPLATE_ARGS = {
    "name": "ChatStream",
    "messages": [
        SystemChatPrompt(
            "You are a helpful AI assistant that helps people with answering questions about planning "
            "permission.<br> If you can't find the answer in the search result below, just say (in Swedish) "
            "\"Tyvärr kan jag inte svara på det.\" Don't try to make up an answer.<br> If the "
            "question is not related to the context, politely respond that you are tuned to only "
            "answer questions that are related to the context.<br> The questions are going to be "
            "asked in Swedish. Your response must always be in Swedish."
        ),
        UserChatPrompt("{query}"),
        UserChatPrompt("Here are the results of the search:\n\n {results}"),
    ],
    "input_map_fn": lambda input: {
        "query": list(input)[0]['query'],
        "results": ' | '.join([doc for doc, _ in list(input)[0]['results']])
    },
    "settings": {
        "model": os.environ.get("CHAT_MODEL", "gpt-4"),
        "temperature": 0
    },
}

SCORING_PROMPT_TEMPLATE_ARGS = {
    "name": "ScoringStream",
    "messages": [
        SystemChatPrompt(
            "You are a scoring systems that classifies documents from 0-100 based on how well they answer a query."),
        UserChatPrompt("Query: {query}\n\nDocument: {document}"),
    ],
    "input_map_fn": lambda input: {**(input)},
    "settings": {
        "model": os.environ.get("SCORING_MODEL", "gpt-3.5-turbo"),
        "temperature": 0,
        "functions": [
            {
                "name": "score_document",
                "description": "Scores the previous document according to the user query\n\n    Parameters\n    ----------\n    score\n        A number from 0-100 scoring how well does the document matches the query. The higher the score, the better match for the query\n    ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                        }
                    },
                    "required": ["score"],
                }
            }
        ],
        "function_call": {"name": "score_document"},
    },
}
