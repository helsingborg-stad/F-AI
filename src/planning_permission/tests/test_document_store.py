import unittest
from typing import AsyncGenerator, Any
from unittest.mock import patch

from planning_permission.store.database import AbstractEmbeddingsDatabase
from planning_permission.store.document_store import DocumentStore
from planning_permission.utils.embeddings_handler import AbstractEmbeddingsGenerator
from planning_permission.utils.file_handler import DocumentHandler


class FakeEmbeddingsDatabase(AbstractEmbeddingsDatabase):
    def __init__(self):
        self.document_chunks = []
        self.embeddings = []

    def add_embeddings(self, document_chunks, embeddings) -> None:
        self.document_chunks.extend(document_chunks)
        self.embeddings.extend(embeddings)

    async def query_embedding(self, embedding, n_results) -> AsyncGenerator[str, Any]:
        for chunk in self.document_chunks[:n_results]:
            yield chunk


class FakeEmbeddingsGenerator(AbstractEmbeddingsGenerator):
    def create_embeddings(self, query):
        return f"fake_embedding_for_{query}"


class TestDocumentStore(unittest.TestCase):

    def setUp(self):
        self.db = FakeEmbeddingsDatabase()
        self.embeddings_generator = FakeEmbeddingsGenerator()
        self.document_store = DocumentStore(self.db, self.embeddings_generator)

    def test_load_document(self):
        with patch.object(DocumentHandler, "convert_docs_to_chunks", return_value=["chunk1", "chunk2"]):
            self.document_store.load_document("test", 512)
            self.assertEqual(self.db.document_chunks, ["chunk1", "chunk2"])
            self.assertEqual(self.db.embeddings, ["fake_embedding_for_chunk1", "fake_embedding_for_chunk2"])

    def test_generate_embeddings(self):
        result = self.document_store.generate_embeddings(["chunk1", "chunk2"])
        self.assertEqual(result, ["fake_embedding_for_chunk1", "fake_embedding_for_chunk2"])

    def test_add_embeddings(self):
        self.document_store.add_embeddings(["chunk1", "chunk2"], ["embedding1", "embedding2"])
        self.assertEqual(self.db.document_chunks, ["chunk1", "chunk2"])
        self.assertEqual(self.db.embeddings, ["embedding1", "embedding2"])

    def test_query(self):
        self.db.document_chunks = ["chunk1", "chunk2"]

        async def run_query():
            results = [res async for res in self.document_store.query("query", 2)]
            self.assertEqual(results, ["chunk1", "chunk2"])

        run_query()


if __name__ == '__main__':
    unittest.main()
