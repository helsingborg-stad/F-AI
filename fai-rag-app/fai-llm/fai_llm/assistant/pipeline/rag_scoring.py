# from typing import Any
#
# from langstream import Stream
#
# from fai_llm.assistant.protocol import IAssistantPipelineStrategy, IAssistantContextStore
#
# from fai_llm.llm.service import create_rag_stream
#
#
# class RagScoringPipeline(IAssistantPipelineStrategy):
#     async def create_pipeline(
#             self,
#             context_store: IAssistantContextStore
#     ) -> Stream[list[str], str]:
#         async def run_rag_stream(query: list[str]):
#             collection_id = context_store.get_mutable().files_collection_id
#             stream = await create_rag_stream(query[0], collection_id)
#             async for r in stream(query[0]):
#                 yield r
#
#         def rag_postprocess(in_data: Any):
#             results: list[str] = in_data[0]['results']
#             concatenated = "\n".join([s for (s, _) in results])
#             context_store.get_mutable().rag_output = concatenated
#             return concatenated
#
#         return (
#             Stream('RAGStream', run_rag_stream)
#             .and_then(rag_postprocess)
#         )
