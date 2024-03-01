import asyncio
from typing import AsyncGenerator, Iterable, List, Tuple

from langstream import Stream, join_final_output, as_async_generator
from langstream.contrib import OpenAIChatStream, OpenAIChatMessage, OpenAIChatDelta

SYSTEM_TEMPLATE = "You are a helpful AI assistant that helps people with answering questions about planning "
"permission.<br> If you can't find the answer in the search result below, just say (in Swedish) "
"\"Tyvärr kan jag inte svara på det.\" Don't try to make up an answer.<br> If the "
"question is not related to the context, politely respond that you are tuned to only "
"answer questions that are related to the context.<br> The questions are going to be "
"asked in Swedish. Your response must always be in Swedish."


async def ask_llm_question(question: str):
    llm_stream: Stream[str, str] = OpenAIChatStream[str, OpenAIChatDelta](
        "RecipeStream",
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


async def ask_llm_raq_question(question: str):
    add_document, list_documents = (lambda documents: (
        lambda document: (documents.append(document), document)[1],
        lambda: [*documents]
    ))([])

    def retrieve_documents(query: str, n_results: int) -> AsyncGenerator[str, None]:
        mock_results = [
            "Document 1",
            "Document 2",
            "Document 3"
        ][0:n_results]

        return as_async_generator(*mock_results)

    def stream(query):
        return (
            Stream[str, str](
                "RetrieveDocumentsStream",
                lambda query: retrieve_documents(query, n_results=3)
            )
            .map(add_document)
            # .map(lambda document: {"query": query, "document": document})
            # .gather()
            # .and_then(lambda results: {"query": query, "results": results[0]})
            .and_then(
                OpenAIChatStream[Iterable[List[Tuple[str, int]]], OpenAIChatDelta](
                    "AnswerStream",
                    lambda results: [
                        OpenAIChatMessage(
                            role="system",
                            content=SYSTEM_TEMPLATE,
                        ),
                        OpenAIChatMessage(role="user", content=query),
                        OpenAIChatMessage(
                            role="user",
                            # content=f"Here are the results of the search:\n\n {' | '.join([doc for doc, _ in list(results)[0]])}",
                            content=f"Here are the results of the search:\n\n Det behövs ingen bygglov för att sätta upp en flaggstång. Det är däremot viktigt att tänka på att flaggstången inte får vara högre än 12 meter. Om flaggstången är högre än 3 meter behöver du anmäla detta till kommunen. Det är också viktigt att tänka på att flaggstången inte får placeras så att den skymmer sikten för trafikanter eller för grannar. Om du är osäker på om du behöver anmäla flaggstången eller inte kan du kontakta kommunen för att få hjälp.",
                        ),
                    ],
                    model="gpt-4",
                    temperature=0,
                ).map(lambda delta: delta.content)
            )
        )(query)

    return await join_final_output(stream(question))
