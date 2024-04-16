from abc import abstractmethod, ABC

import magic
from unstructured.partition.md import partition_md
from unstructured.partition.pdf import partition_pdf


class AbstractDocumentParser(ABC):
    @abstractmethod
    def parse(self, filename: str):
        pass


class PDFParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_pdf(filename, chunking_strategy="basic")


class MarkdownParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_md(filename)


class ParserFactory:
    @staticmethod
    def get_parser(file_path: str) -> AbstractDocumentParser:
        mime_type = magic.from_file(file_path, mime=True)

        if mime_type == 'application/pdf':
            return PDFParser()
        if mime_type == 'text/markdown':
            return MarkdownParser()

        raise ValueError(f'Unsupported file type: {mime_type}')
