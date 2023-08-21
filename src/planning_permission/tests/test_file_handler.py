import unittest
from unittest.mock import MagicMock
from planning_permission.utils.file_handler import DocumentHandler, AbstractDocumentParser


class TestChunkStringsMethod(unittest.TestCase):
    def setUp(self):
        self.document_handler = DocumentHandler()

    def test_chunk_strings(self):
        strings = [
            "This is a test sentence with eight words.",
            "Another test sentence with six words.",
            "Yet another test sentence with seven words.",
            "Final test sentence with six words."
        ]
        expected_output = [
            "This is a test sentence with eight words.",
            "Another test sentence with six words.",
            "Yet another test sentence with seven words.",
            "Final test sentence with six words."
        ]

        result = self.document_handler.chunk_strings(strings, max_words=9)
        self.assertEqual(result, expected_output)

    def test_empty_input(self):
        strings = []
        expected_output = []

        result = self.document_handler.chunk_strings(strings, max_words=11)
        self.assertEqual(result, expected_output)

    def test_no_split(self):
        strings = [
            "This is a test sentence with eight words.",
            "Another test sentence with six words."
        ]
        expected_output = [
            "This is a test sentence with eight words.\nAnother test sentence with six words."
        ]

        result = self.document_handler.chunk_strings(strings, max_words=20)
        self.assertEqual(result, expected_output)


class FakeMarkdownParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return [f"Markdown element from {filename}"]


class FakePDFParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return [f"PDF element from {filename}"]


class FakeDocumentParserFactory:
    def create_parser(self, file_extension: str):
        if file_extension == "md":
            return FakeMarkdownParser()
        elif file_extension == "pdf":
            return FakePDFParser()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")


class TestParseDocsMethod(unittest.TestCase):
    def setUp(self):
        self.handler = DocumentHandler()

    def test_parse_docs(self):
        documents = ["file1.md", "file2.pdf"]
        fake_parser_factory = FakeDocumentParserFactory()

        # Replace the print function with a mock object to avoid side effects
        with unittest.mock.patch("builtins.print", new_callable=unittest.mock.MagicMock) as mock_print:
            result = self.handler.parse_docs(documents, fake_parser_factory)

        self.assertEqual(
            result,
            [
                "Markdown element from file1.md",
                "PDF element from file2.pdf",
            ],
        )
        mock_print.assert_any_call("Parsing file1.md...")
        mock_print.assert_any_call("Parsing file2.pdf...")


if __name__ == '__main__':
    unittest.main()