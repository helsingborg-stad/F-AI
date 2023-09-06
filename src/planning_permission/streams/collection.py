import json
from langstream import Stream
from langstream.contrib import OpenAIChatDelta, OpenAIChatMessage, OpenAIChatStream

class ROLE:
    USER = 'user'
    SYSTEM = 'system'
    
def score_stream_factory(query: str, settings = {}) -> Stream[str, int]:
    return OpenAIChatStream[str, OpenAIChatDelta](
        "ScoreDocumentStream",
        lambda document: [
            OpenAIChatMessage(
                content=content.format(**{"query": query, "document": document}), 
                role=role
            )
            for role, content
            in [
                [
                    ROLE.SYSTEM,
                    """
                        You are a scoring systems that classifies documents from 0-100 based on how well they answer a query
                    """
                ],
                [
                    ROLE.USER,
                    """
                        Query: {query}
                        Document: {document}
                    """
                ],
            ]
        ],
        ** {
            "model": "gpt-3.5-turbo",
            "temperature": 0,
            "functions": [
                {
                    "name": "score_document",
                    "description": "Scores the previous document according to the user query\n\n    Parameters\n    ----------\n    score\n        A number from 0-100 scoring how well does the document matches the query. The higher the score, the better match for the query\n",
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
            ** settings
        }
    ).map(
        lambda delta: (lambda score: score)(**json.loads(delta.content))
        if delta.role == "function" and delta.name == "score_document"
        else 0
    )


def chat_stream_factory(query: str, settings = {}) -> OpenAIChatStream[str, OpenAIChatDelta]:
    return OpenAIChatStream[str, OpenAIChatDelta](
        "QAChatStream",
        lambda context: [
            OpenAIChatMessage(
                content=content.format(**{"query": query, "context": context}), 
                role=role
            )
            for role, content
            in [
                [
                    ROLE.SYSTEM,
                    """
                        You are a helpful AI assistant that helps people with answering questions about planning permission.
                        If you can't find the answer in the search result below, just say (in Swedish) "Tyvärr kan jag inte svara på det."
                        Don't try to make up an answer. If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
                        The questions are going to be asked in Swedish. Your response must always be in Swedish.
                    """
                ],
                [
                    ROLE.USER,
                    """
                        {query}
                    """
                ],
                [
                    ROLE.SYSTEM,
                    """
                        ## Search results:
                        ```
                        {context}
                        ´´´
                    """
                ],    
            ]
        ],
        ** {
            "model": "gpt-4",
            "temperature": 0,
            ** settings
        }
    )
    
def document_stream_factory(query: str, store, n_per_q=2) -> Stream[str, str]:
    return Stream[str, str](
        "DocumentStream",
        lambda _: store.query(query, n_results=n_per_q),
    )