from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from typing import Any
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
from fai_backend.logger.console import console


def error_handler(default_return: Any = None):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                console.log(f'Error in {func.__name__}:\n{e}')
                return default_return

        return wrapper

    return decorator


def is_url(string: str) -> bool:
    parsed = urlparse(string)
    return parsed.scheme in {'http', 'https'}


@error_handler(default_return='null')
def get_mime_type(file_path: str) -> str:
    if is_url(file_path):
        return magic.from_buffer(requests.get(file_path, verify=settings.ENV_MODE != 'development').content, mime=True)
    return magic.from_file(file_path, mime=True)


class AbstractDocumentParser(ABC):
    @abstractmethod
    def parse(self, filename: str) -> list[Element]:
        pass


class DocxParser(AbstractDocumentParser):
    @error_handler(default_return=[])
    def parse(self, filename: str) -> list[Element]:
        if is_url(filename):
            return partition_docx(
                url=filename,
                ssl_verify=settings.ENV_MODE != 'development',
                chunking_strategy='basic'
            )
        return partition_docx(filename, chunking_strategy='basic')


class PDFParser(AbstractDocumentParser):
    @error_handler(default_return=[])
    def parse(self, filename: str) -> list[Element]:
        if is_url(filename):
            return partition_pdf(
                url=filename,
                ssl_verify=settings.ENV_MODE != 'development',
                chunking_strategy='basic'
            )
        return partition_pdf(filename, chunking_strategy='basic')


class MarkdownParser(AbstractDocumentParser):
    @error_handler(default_return=[])
    def parse(self, filename: str) -> list[Element]:
        if is_url(filename):
            return partition_md(
                url=filename,
                ssl_verify=settings.ENV_MODE != 'development',
                chunking_strategy='basic'
            )
        return partition_md(filename, chunking_strategy='basic')


class ExcelParser(AbstractDocumentParser):
    @error_handler(default_return=[])
    def parse(self, filename: str) -> list[Element]:
        if is_url(filename):
            return partition_xlsx(
                url=filename,
                ssl_verify=settings.ENV_MODE != 'development'
            )
        return partition_xlsx(filename)


class HTMLParser(AbstractDocumentParser):
    @staticmethod
    def _parse_html(filename: str) -> list[Element]:
        if is_url(filename):
            return partition_html(
                url=filename,
                ssl_verify=settings.ENV_MODE != 'development',
                chunking_strategy='basic'
            )
        return partition_html(filename, chunking_strategy='basic')

    @error_handler(default_return=[])
    def parse(self, filename: str) -> list[Element]:
        chunks = self._parse_html(filename)
        title = chunks[0].metadata.orig_elements[0].text if len(chunks) > 0 else None
        for chunk in chunks:
            chunk.metadata.page_name = title
        return chunks


class NullParser(AbstractDocumentParser):
    def parse(self, filename: str) -> list[Element]:
        return []


class ParserFactory:
    MIME_TYPE_MAPPING: dict[str, type[AbstractDocumentParser]] = {
        'application/pdf': PDFParser,
        'text/plain': MarkdownParser,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxParser,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelParser,
        'text/html': HTMLParser,
        'null': NullParser
    }

    @staticmethod
    def get_parser(file_path: str) -> AbstractDocumentParser:
        console.log(f'Getting parser for file: {file_path}')
        mime_type = get_mime_type(file_path)
        parser_cls = ParserFactory.MIME_TYPE_MAPPING.get(mime_type)

        if parser_cls is None:
            console.log(f'Unsupported file type: {mime_type}')
            return NullParser()

        return parser_cls()
