from pathlib import Path
from typing import Any, Protocol

import magic
from pypdf import PdfReader
from unstructured.documents.elements import Element
from unstructured.partition.docx import partition_docx
from unstructured.partition.md import partition_md
from unstructured.partition.pdf import partition_pdf

from fai_backend.config import settings


class IDocumentParser(Protocol):
    @staticmethod
    def parse(file_path: Path) -> Any:
        ...


class DocxParser:
    def parse(self, filename: str):
        return partition_docx(filename, chunking_strategy='basic')


class PDFParserDefault:
    @staticmethod
    def parse(file_path: Path) -> list[str]:
        reader = PdfReader(file_path)
        return [page.extract_text() for page in reader.pages]


class PDFParserUnstructured:
    @staticmethod
    def parse(filename: str) -> list[Element]:
        return partition_pdf(filename, chunking_strategy='basic')


class MarkdownParserDefault:
    @staticmethod
    def parse(filename: str):
        return partition_md(filename)


class ParserFactory:
    parsers = {
        'default': {
            'application/pdf': PDFParserDefault,
            'text/plain': MarkdownParserDefault,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxParser},
        'unstructured': {
            'application/pdf': PDFParserUnstructured,
            'text/plain': MarkdownParserDefault,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxParser}}

    @staticmethod
    def get_parser(file_path: Path) -> IDocumentParser:
        env = settings.FILE_PARSER
        parser = ParserFactory.parsers.get(env, 'default')
        file_mime_type = magic.from_file(file_path, mime=True)

        if file_mime_type not in parser:
            raise ValueError(f'Mime type: {file_mime_type} not supported')

        return parser[file_mime_type]()
