import unittest

from planning_permission.utils.embeddings_handler import Embeddings, AbstractEmbeddingsGenerator


class FakeEmbeddingsGenerator(AbstractEmbeddingsGenerator):
    def create_embeddings(self, query):
        return f"embedding-{query}"


class TestFromChunksMethod(unittest.TestCase):
    def setUp(self):
        self.embeddings = Embeddings()
        self.fake_generator = FakeEmbeddingsGenerator()

    def test_from_chunks(self):
        chunks = ["chunk1", "chunk2", "chunk3"]
        expected_output = [
            "embedding-chunk1",
            "embedding-chunk2",
            "embedding-chunk3"
        ]

        result = self.embeddings.from_chunks(self.fake_generator, chunks)
        self.assertEqual(result, expected_output)

    def test_empty_input(self):
        chunks = []
        expected_output = []

        result = self.embeddings.from_chunks(self.fake_generator, chunks)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
