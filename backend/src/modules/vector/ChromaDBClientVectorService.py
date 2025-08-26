import chromadb
from chromadb import EmbeddingFunction, AsyncClientAPI
from chromadb.errors import InvalidCollectionException
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction

from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey
from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.models.VectorSpace import VectorSpace
from src.modules.vector.protocols.IVectorService import IVectorService


class ChromaDBClientVectorService(IVectorService):
    def __init__(self, settings_service: ISettingsService, host: str, port: int):
        self._chroma_client = None
        self._settings_service = settings_service
        self._host = host
        self._port = port

    async def _get_client(self) -> AsyncClientAPI:
        if self._chroma_client is None:
            self._chroma_client = await chromadb.AsyncHttpClient(self._host, self._port, settings=chromadb.Settings(
                anonymized_telemetry=False,
                allow_reset=True
            ))
        return self._chroma_client

    async def create_vector_space(self, space: str, embedding_model: str):
        embedding_function = await self._get_embedding_function(embedding_model)
        client = await self._get_client()
        try:
            await client.get_collection(space, embedding_function)
        except InvalidCollectionException:
            await client.create_collection(
                name=space,
                embedding_function=embedding_function,
            )

    async def add_documents_to_vector_space(self, space: str, embedding_model: str, documents: list[VectorDocument]):
        if len(documents) == 0:
            return

        client = await self._get_client()

        collection = await client.get_collection(
            space,
            embedding_function=await self._get_embedding_function(embedding_model)
        )

        await collection.add(
            documents=[doc.content for doc in documents],
            ids=[doc.id for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )

    async def delete_vector_space(self, space: str):
        try:
            client = await self._get_client()
            await client.delete_collection(space)
        except ValueError:
            return

    async def get_vector_spaces(self) -> list[VectorSpace]:
        client = await self._get_client()
        return [VectorSpace(name=collection) for collection in await client.list_collections()]

    async def query_vector_space(
            self,
            space: str,
            embedding_model: str,
            query: str,
            max_results: int
    ) -> list[VectorDocument]:
        try:
            client = await self._get_client()
            collection = await client.get_collection(space, embedding_function=await self._get_embedding_function(
                embedding_model))
        except InvalidCollectionException:
            return []

        query_results = await collection.query(
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

    async def _get_embedding_function(self, embedding_model_name: str) -> EmbeddingFunction:
        openai_api_key = await self._settings_service.get_setting(SettingKey.OPENAI_API_KEY.key)
        embedding_model_map = {
            'default': lambda: embedding_functions.DefaultEmbeddingFunction(),
            'text-embedding-3-small': lambda: OpenAIEmbeddingFunction(
                api_key=openai_api_key,
                model_name='text-embedding-3-small'
            )
        }
        return embedding_model_map[embedding_model_name or 'default']()
