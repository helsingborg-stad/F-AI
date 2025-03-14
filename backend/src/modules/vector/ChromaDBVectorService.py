import os

import chromadb
from chromadb import EmbeddingFunction
from chromadb.errors import InvalidCollectionException
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from chromadb.utils import embedding_functions

from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.models.VectorSpace import VectorSpace
from src.modules.vector.protocols.IVectorService import IVectorService


class ChromaDBVectorService(IVectorService):
    def __init__(self, db_path='./__chromadb'):
        self._chroma_client = chromadb.PersistentClient(
            path=db_path,
            settings=chromadb.Settings(
                anonymized_telemetry=False,
                allow_reset=True
            ),
        )

    async def create(self, space: str, embedding_model: str):
        embedding_function = self._get_embedding_function(embedding_model)
        try:
            self._chroma_client.get_collection(space, embedding_function)
        except InvalidCollectionException:
            self._chroma_client.create_collection(
                name=space,
                embedding_function=embedding_function,
            )

    async def add_to(self, space: str, embedding_model: str, documents: list[VectorDocument]):
        if len(documents) == 0:
            return

        collection = self._chroma_client.get_collection(
            space,
            embedding_function=self._get_embedding_function(embedding_model)
        )

        collection.add(
            documents=[doc.content for doc in documents],
            ids=[doc.id for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )

    async def delete(self, space: str):
        try:
            self._chroma_client.delete_collection(space)
        except ValueError:
            return

    async def list_spaces(self) -> list[VectorSpace]:
        return [VectorSpace(name=collection) for collection in self._chroma_client.list_collections()]

    async def query(self, space: str, embedding_model: str, query: str, max_results: int) -> list[VectorDocument]:
        try:
            collection = self._chroma_client.get_collection(space, embedding_function=self._get_embedding_function(
                embedding_model))
        except InvalidCollectionException:
            return []

        query_results = collection.query(
            query_texts=[query],
            n_results=max_results
        )

        ids = query_results['ids'][0]
        documents = query_results['documents'][0]
        metadatas = query_results['metadatas'][0]

        return [VectorDocument(
            id=ids[i],
            content=documents[i],
            metadata=dict(metadatas[i]) if metadatas[i] else None
        ) for i in range(len(ids))
        ]

    @staticmethod
    def _get_embedding_function(embedding_model_name: str) -> EmbeddingFunction:
        embedding_model_map = {
            'default': lambda: embedding_functions.DefaultEmbeddingFunction(),
            'text-embedding-3-small': lambda: OpenAIEmbeddingFunction(
                api_key=os.environ['OPENAI_API_KEY'],
                model_name='text-embedding-3-small'
            )
        }
        return embedding_model_map[embedding_model_name or 'default']()
