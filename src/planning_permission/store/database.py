from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

import chromadb
from langstream import as_async_generator


class AbstractEmbeddingsDatabase(ABC):
    """
    Abstract base class for an embedding´s database.

    Methods
    -------
    add_embeddings(document_chunks: Any, embeddings: Any) -> None:
        Abstract method to add embeddings to the database.

    query_embedding(embedding: Any, n_results: int) -> AsyncGenerator[str, Any]:
        Abstract method to query an embedding from the database.

    is_collection_empty() -> bool:
        Abstract method to check if the collection in the database is empty.
    """

    @abstractmethod
    def add_embeddings(self, document_chunks, embeddings) -> None:
        """
        Abstract method to add embeddings to the database.

        Parameters
        ----------
        document_chunks : Any
            The document chunks to add to the database.

        embeddings : Any
            The embeddings to add to the database.
        """
        pass

    @abstractmethod
    def query_embedding(self, embedding, n_results) -> AsyncGenerator[str, Any]:
        """
        Abstract method to query an embedding from the database.

        Parameters
        ----------
        embedding : Any
            The embedding to query.

        n_results : int
            The number of results to return.

        Returns
        -------
        AsyncGenerator[str, Any]
            An async generator yielding the query results.
        """
        pass

    @abstractmethod
    def is_collection_empty(self):
        """
        Abstract method to check if the collection in the database is empty.

        Returns
        -------
        bool
            True if the collection is empty, False otherwise.
        """
        pass


class ChromaDB(AbstractEmbeddingsDatabase):
    """
    Concrete class for an embeddings database using ChromaDB.

    Methods
    -------
    __init__(db_directory: str, collection_name: str):
        Initializes the ChromaDB embeddings database.

    is_collection_empty() -> bool:
        Checks if the collection in the database is empty.

    add_embeddings(document_chunks: Any, embeddings: Any) -> None:
        Adds embeddings to the database.

    query_embedding(embedding: Any, n_results: int) -> AsyncGenerator[str, Any]:
        Queries an embedding from the database.

    Inherits
    --------
    AbstractEmbeddingsDatabase
    """

    def __init__(self, db_directory: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=db_directory,
            settings=chromadb.Settings(anonymized_telemetry=False)  # opt out of telemetry
        )
        self.collection = self.client.get_or_create_collection(collection_name)

    def is_collection_empty(self):
        return self.collection.count() == 0

    def add_embeddings(self, document_chunks, embeddings) -> None:
        embeddings and self.collection.add(
            documents=document_chunks,
            embeddings=embeddings,
            ids=[str(i) for i, _ in enumerate(document_chunks)],
        )

    def query_embedding(self, embedding, n_results) -> AsyncGenerator[str, Any]:
        results = self.collection.query(
            query_embeddings=embedding,
            n_results=n_results,
        )["documents"]

        results = results[0]  # type: ignore
        return as_async_generator(*results)
