import json
from typing import Any, AsyncGenerator

from langstream import Stream

from fai_backend.assistant.protocol import IAssistantPipelineStrategy, IAssistantContextStore
from fai_backend.collection.dependencies import get_collection_service
from fai_backend.llm.service import query_vector
from fai_backend.projects.dependencies import get_project_service
from fai_backend.vector.factory import vector_db
from fai_backend.vector.service import VectorService


class RagScoringPipeline(IAssistantPipelineStrategy):
    async def create_pipeline(
            self,
            context_store: IAssistantContextStore
    ) -> Stream[list[str], str]:
        async def run_rag_stream(query: list[str]):
            collection_id = context_store.get_mutable().files_collection_id
            vector_service = VectorService(vector_db=vector_db, collection_meta_service=get_collection_service())
            vector_db_query_result = await query_vector(
                vector_service=vector_service,
                collection_name=collection_id,
                query=query[0],
            )

            documents: [str] = []

            def store_and_return_document(document: str):
                documents.append(document)
                return document

            def append_score_to_documents(scores):
                z = zip(documents, [s[0] for s in scores])
                return z

            def sort_and_slice_documents(scored_documents, slice_size: int):
                first_element = list(scored_documents)[0]
                sorted_scores = sorted(first_element, key=lambda x: x[1], reverse=True)
                return sorted_scores[:slice_size]

            projects = await get_project_service().read_projects()
            scoring_template = next(a for a in projects[0].assistants if a.id == '_rag_scoring')
            from fai_backend.assistant.assistant import Assistant
            from fai_backend.assistant.service import InMemoryAssistantContextStore

            async def scoring_stream(document: str) -> AsyncGenerator[str, None]:
                scoring_context_store = InMemoryAssistantContextStore()
                assistant = Assistant(scoring_template, scoring_context_store)
                stream = await assistant.create_stream()
                scoring_context_store.get_mutable().rag_document = document

                full = ""
                async for o in stream(query[0]):
                    if o.final:
                        full += o.data

                score = json.loads(full)['score']
                yield score

            full_stream = (
                vector_db_query_result
                .map(store_and_return_document)
                .map(scoring_stream)
                .gather()
                .and_then(append_score_to_documents)
                .and_then(lambda scored_documents: sort_and_slice_documents(scored_documents, 6))
                .and_then(lambda results: {"query": query, "results": results[0]})
            )

            async for r in full_stream(query[0]):
                yield r

        def rag_postprocess(in_data: Any):
            results: list[str] = in_data[0]['results']
            concatenated = "\n".join([s for (s, _) in results])
            context_store.get_mutable().rag_output = concatenated
            return concatenated

        return (
            Stream('RAGStream', run_rag_stream)
            .and_then(rag_postprocess)
        )
