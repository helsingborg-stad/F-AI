import json
from typing import Callable
from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatMessage, OpenAIChatDelta

class ROLE:
    SYSTEM = "system"
    USER = "user"

def get_scoring_stream(query: str) -> Callable:
    def score_document(score: int) -> int:
        return score

    scoring_stream: Stream[str, int] = OpenAIChatStream[str, OpenAIChatDelta](
        "AnswerStream",
        lambda document: [
            OpenAIChatMessage(
                role=role,
                content=content.format(query=query, document=document),
            )
            for role, content
            in [
                [ROLE.SYSTEM, 
                    "You are a scoring systems that classifies documents from 0-100 based on how well they answer a query"
                ],
                [ROLE.USER, 
                    "Query: {query}\n\nDocument: {document}"
                ],
            ]
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        functions=[
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
        function_call={"name": "score_document"},
    ).map(
        lambda delta: score_document(**json.loads(delta.content))
        if delta.role == "function" and delta.name == "score_document"
        else 0
    )

    return scoring_stream

def get_query_openai(query: str) -> Callable:
    query_openai: OpenAIChatStream[str, OpenAIChatDelta] = OpenAIChatStream[str, OpenAIChatDelta](
        "ChatStream",
        lambda results: [
            OpenAIChatMessage(role=role, content=content.format(query=query, results=' | '.join([doc for doc, _ in list(results)[0]])))
            for role, content
            in [
                [ROLE.SYSTEM, 
                    "You are a helpful AI assistant that helps people with answering questions about planning "
                    "permission.<br> If you can't find the answer in the search result below, just say (in Swedish) "
                    "\"Tyvärr kan jag inte svara på det.\" Don't try to make up an answer.<br> If the "
                    "question is not related to the context, politely respond that you are tuned to only "
                    "answer questions that are related to the context.<br> The questions are going to be "
                    "asked in Swedish. Your response must always be in Swedish."
                ],
                [ROLE.USER, "{query}"],
                [ROLE.USER, "Here are the results of the search:\n\n {results}"],
            ]
        ],
        model="gpt-4",
        temperature=0,
    )

    return query_openai
