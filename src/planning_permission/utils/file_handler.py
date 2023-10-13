import asyncio
import glob
import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type, Union, Dict

from unstructured.partition.md import partition_md
from unstructured.partition.pdf import partition_pdf
import chainlit as cl

from planning_permission.utils.command_registry import ICommandSetup


@dataclass
class FileObject:
    name: str
    path: str
    size: int
    type: str
    content: bytes


class AbstractDocumentParser(ABC):
    """
    Abstract base class for parsing documents. This class requires
    subclasses to implement the `parse` method.

    Methods
    -------
    parse(filename: str) -> Any
        Abstract method to parse a document from the given filename.
    """

    @abstractmethod
    def parse(self, filename: str):
        pass


class AbstractUploadedFileHandler(ABC):
    @abstractmethod
    async def handle_uploaded_files(self, files: list[FileObject]) -> None:
        pass


class MarkdownParser(AbstractDocumentParser):
    """
    Class for parsing Markdown documents.

    Methods
    -------
    parse(filename: str) -> Any
        Parses a Markdown document from the given filename.

    Inherits
    --------
    AbstractDocumentParser
    """

    def parse(self, filename: str):
        return partition_md(filename=filename)


class PDFParser(AbstractDocumentParser):
    """
    Class for parsing PDF documents.

    Methods
    -------
    parse(filename: str) -> Any
        Parses a PDF document from the given filename.

    Inherits
    --------
    AbstractDocumentParser
    """

    def parse(self, filename: str):
        return partition_pdf(filename=filename)


class DocumentParserFactory:
    """
    Factory class for creating document parsers.

    Methods
    -------
    create_parser(file_extension: str) -> AbstractDocumentParser
        Returns an instance of the appropriate document parser based on the file extension.

    Raises
    ------
    ValueError
        If an unsupported file extension is provided.
    """

    def create_parser(self, file_extension: str) -> AbstractDocumentParser:
        if file_extension == "md":
            return MarkdownParser()
        elif file_extension == "pdf":
            return PDFParser()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")


class DocumentHandler:
    """
    Class for handling and processing documents.

    Methods
    -------
    load_files_recursive(pathname: str) -> List[str]
        Returns a list of file paths matching the given pathname pattern.

    chunk_strings(lst: List[str], max_words: int) -> List[str]
        Splits a list of strings into chunks based on the maximum number of words.

    parse_docs(documents: List[str], parser_factory: DocumentParserFactory) -> List[Type[AbstractDocumentParser]]
        Parses a list of documents using the provided parser factory.

    convert_docs_to_chunks(pathname: str, max_words: int, parser_factory: DocumentParserFactory) -> List[str]
        Converts documents to chunks of text with a maximum number of words.
    """

    def load_files_recursive(self, pathname: str) -> List[str]:
        return glob.glob(pathname, recursive=True)

    def chunk_strings(self, lst, max_words) -> List[str]:
        chunks, chunk, count = [], [], 0
        for s in lst:
            words = len(s.split())
            if count + words <= max_words:
                chunk.append(s)
                count += words
            else:
                chunks.append(chunk)
                chunk, count = [s], words
        if chunk:
            chunks.append(chunk)
        return ["\n".join(chunk) for chunk in chunks]

    def parse_docs(self, documents: List[str], parser_factory) -> List[Type[AbstractDocumentParser]]:
        elements = []
        for document in documents:
            print(f"Parsing {document}...")
            parser = parser_factory.create_parser(document.split('.')[-1])
            elements += parser.parse(document)

        return elements

    def convert_docs_to_chunks(self, pathname, max_words, parser_factory: DocumentParserFactory) -> List[str]:
        documents = self.load_files_recursive(pathname)
        parsed_documents = self.parse_docs(documents, parser_factory)
        return self.chunk_strings([str(elem) for elem in parsed_documents], max_words=max_words)


class FileUpload(AbstractUploadedFileHandler):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def save_file(self, file_objects: list[FileObject], destination_directory: str):
        os.makedirs(destination_directory, exist_ok=True)

        for file_object in file_objects:
            file_path = os.path.join(destination_directory, file_object.name)

            with open(file_path, "wb") as file:
                file.write(file_object.content)

    async def handle_uploaded_files(self, files: list[FileObject]) -> None:
        self.save_file(file_objects=files, destination_directory=self.storage_path)


class ChainlitFile:
    async def upload(
            self,
            accepted_mime_types: Union[List[str], Dict[str, List[str]]],
            uploaded_file_handler: AbstractUploadedFileHandler,
            max_size_mb: int = 2,
            max_files: int = 1,
            timeout: int = 60,
            rise_on_timeout: bool = False,
    ):
        files = None

        while files is None:
            files = await cl.AskFileMessage(
                content=f"Please upload a file. If no file is uploaded within {timeout} seconds, "
                        f"the file upload will be cancelled.",
                accept=accepted_mime_types,
                max_size_mb=max_size_mb,
                max_files=max_files,
                timeout=timeout,
                raise_on_timeout=rise_on_timeout
            ).send()

        file_objects = [FileObject(
            name=file.name,
            path=file.path,
            size=file.size,
            type=file.type,
            content=file.content
        ) for file in files]

        await uploaded_file_handler.handle_uploaded_files(file_objects)
