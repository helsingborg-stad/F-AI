import unittest
from unittest.mock import MagicMock, mock_open, patch
from planning_permission.utils.file_handler import DocumentHandler, AbstractDocumentParser, FileUpload, FileObject


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


class TestFileUpload(unittest.TestCase):

    def setUp(self):
        self.storage_path = "/path/to/storage"
        self.file_upload = FileUpload(self.storage_path)

    def test_save_file(self):
        file_objects = [
            FileObject(name="file1.txt", path="", size=15, type="text/plain", content=b"Hello, world!"),
            FileObject(name="file2.txt", path="", size=12, type="text/plain", content=b"Hello, File!"),
        ]
        destination_directory = "/path/to/destination"

        m = mock_open()
        with patch('builtins.open', m), patch('os.makedirs') as mock_makedirs:
            self.file_upload.save_file(file_objects, destination_directory)

        mock_makedirs.assert_called_once_with(destination_directory, exist_ok=True)
        m.assert_any_call('/path/to/destination/file1.txt', 'wb')
        m.assert_any_call('/path/to/destination/file2.txt', 'wb')
        m().write.assert_any_call(b"Hello, world!")
        m().write.assert_any_call(b"Hello, File!")

    def test_handle_uploaded_files(self):
        file_objects = [
            FileObject(name="file3.txt", path="", size=15, type="text/plain", content=b"Hello, world!"),
            FileObject(name="file4.txt", path="", size=12, type="text/plain", content=b"Hello, File!"),
        ]

        with patch.object(self.file_upload, 'save_file') as mock_save_file:
            import asyncio
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(self.file_upload.handle_uploaded_files(file_objects))
            finally:
                loop.close()

        mock_save_file.assert_called_once_with(file_objects=file_objects, destination_directory=self.storage_path)


if __name__ == '__main__':
    unittest.main()
