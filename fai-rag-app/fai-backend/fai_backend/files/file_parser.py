from abc import abstractmethod, ABC

import magic
from unstructured.partition.docx import partition_docx
from unstructured.partition.md import partition_md
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.html import partition_html


class AbstractDocumentParser(ABC):
    @abstractmethod
    def parse(self, filename: str):
        pass


class DocxParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_docx(filename, chunking_strategy="basic")


class PDFParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_pdf(filename, chunking_strategy="basic")


class MarkdownParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_md(filename)


class ExcelParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_xlsx(filename)


class HTMLParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_html(filename)


class ParserFactory:
    @staticmethod
    def get_parser(file_path: str) -> AbstractDocumentParser:
        mime_type = magic.from_file(file_path, mime=True)

        if mime_type == 'application/pdf':
            return PDFParser()
        if mime_type == 'text/plain':
            return MarkdownParser()
        if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return DocxParser()
        if mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            return ExcelParser()
        if mime_type == 'text/html':
            return HTMLParser()

        raise ValueError(f'Unsupported file type: {mime_type}')
