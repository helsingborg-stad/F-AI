from abc import ABC, abstractmethod
from urllib.parse import urlparse

import magic
import requests
from unstructured.documents.elements import Element
from unstructured.partition.docx import partition_docx
from unstructured.partition.html import partition_html
from unstructured.partition.md import partition_md
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.xlsx import partition_xlsx

from fai_backend.config import settings


def is_url(string: str) -> bool:
    parsed = urlparse(string)
    return parsed.scheme in {'http', 'https'}


def get_mime_type(file_path: str) -> str:
    if is_url(file_path):
        return magic.from_buffer(requests.get(file_path, verify=False).content, mime=True)
    return magic.from_file(file_path, mime=True)


class AbstractDocumentParser(ABC):
    @abstractmethod
    def parse(self, filename: str) -> list[Element]:
        pass


class DocxParser(AbstractDocumentParser):
    def parse(self, filename: str) -> list[Element]:
        return partition_docx(filename, chunking_strategy='basic')


class PDFParser(AbstractDocumentParser):
    def parse(self, filename: str) -> list[Element]:
        return partition_pdf(filename, chunking_strategy='basic')


class MarkdownParser(AbstractDocumentParser):
    def parse(self, filename: str) -> list[Element]:
        return partition_md(filename, chunking_strategy='basic')


class ExcelParser(AbstractDocumentParser):
    def parse(self, filename: str) -> list[Element]:
        return partition_xlsx(filename)


class HTMLParser(AbstractDocumentParser):
    def parse(self, filename: str):
        return partition_html(filename)


class ParserFactory:
    MIME_TYPE_MAPPING: dict[str, type[AbstractDocumentParser]] = {
        'application/pdf': PDFParser,
        'text/plain': MarkdownParser,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxParser,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelParser,
        'text/html': HTMLParser,
    }

    @staticmethod
    def get_parser(file_path: str) -> AbstractDocumentParser:
        mime_type = get_mime_type(file_path)
        parser_cls = ParserFactory.MIME_TYPE_MAPPING.get(mime_type)

        if parser_cls is None:
            raise ValueError(f'Unsupported file type: {mime_type}')

        return parser_cls()
