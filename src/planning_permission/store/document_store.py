import asyncio
import os
import time
from typing import AsyncGenerator, Any
from .database import AbstractEmbeddingsDatabase
from planning_permission.utils.embeddings_handler import AbstractEmbeddingsGenerator, Embeddings
from planning_permission.utils.file_handler import DocumentHandler, DocumentParserFactory
from planning_permission.utils.command_registry import ICommandSetup, CommandRegistry
from planning_permission.utils.markdown import MarkdownFormatter


class DocumentStore(ICommandSetup):
    """
    Class for handling documents and their embeddings in a database.

    Attributes
    ----------
    embeddings_db : AbstractEmbeddingsDatabase
        The database that stores the embeddings of the documents.

    embeddings_generator : AbstractEmbeddingsGenerator
        The generator used to create embeddings for the documents.

    Methods
    -------
    __init__(db: AbstractEmbeddingsDatabase, embeddings_generator: AbstractEmbeddingsGenerator):
        Initializes the DocumentStore with the given database and embeddings generator.

    is_collection_empty() -> bool:
        Checks if the collection in the embeddings database is empty.

    load_document(pathname: str, max_words: int = 512) -> None:
        Loads a document, partitions it into chunks, generates embeddings for the chunks, and adds them to the database.

    generate_embeddings(input_chunks: Any) -> Any:
        Generates embeddings for the given input chunks using the embeddings generator.

    add_embeddings(chunks: Any, embeddings: Any) -> None:
        Adds the given chunks and their embeddings to the database.

    query(query: str, n_results: int) -> AsyncGenerator[str, Any]:
        Queries the database with the given query and returns the results as an async generator.
    """

    def __init__(
            self, db: AbstractEmbeddingsDatabase,
            embeddings_generator: AbstractEmbeddingsGenerator,
            file_loader_callback
    ):
        self.embeddings_db = db
        self.embeddings_generator = embeddings_generator
        self.file_loader_callback = file_loader_callback

    def is_collection_empty(self):
        return self.embeddings_db.is_collection_empty()

    def load_document(self, pathname: str, max_words: int = 512):
        file_handler = DocumentHandler()
        chunks = file_handler.convert_docs_to_chunks(pathname, max_words, DocumentParserFactory())
        print(f"Loaded {len(chunks)} chunks")  # TODO: Remove side effect print

        embeddings = self.generate_embeddings(chunks)
        self.add_embeddings(chunks, embeddings)

    def generate_embeddings(self, input_chunks):
        embeddings_generator = Embeddings()
        return embeddings_generator.from_chunks(self.embeddings_generator, input_chunks)

    def add_embeddings(self, chunks, embeddings):
        self.embeddings_db.add_embeddings(chunks, embeddings)

    def query(self, query: str, n_results: int) -> AsyncGenerator[str, Any]:
        query_as_embedding = self.embeddings_generator.create_embeddings(query)
        return self.embeddings_db.query_embedding(query_as_embedding, n_results)

    def embedding_commands(self, option: str, parameter: str) -> str:
        handlers = {
            "collection": {
                "list": lambda: MarkdownFormatter().collection_to_markdown_table(
                    "Collections",
                    list(self.embeddings_db.list_collections())
                ),
                "reset": lambda: (self.embeddings_db.reset_collections(), "Collections reset")[1],
            }
        }
        handler = handlers.get(option, {}).get(parameter)

        if handler:
            return handler()

        return f"Invalid embeddings command: {option} {parameter}"

    def file_commands(self, option: str) -> str:
        handlers = {
            "upload": lambda: (asyncio.run(self.file_loader_callback()), "Upload complete")[1],
        }
        handlers = handlers.get(option)

        if handlers:
            return handlers()

        return f"Invalid file command: {option}"

    def register_commands(self, command_registry: CommandRegistry):
        command_registry.command('embeddings')(self.embedding_commands)
        command_registry.command('file')(self.file_commands)
