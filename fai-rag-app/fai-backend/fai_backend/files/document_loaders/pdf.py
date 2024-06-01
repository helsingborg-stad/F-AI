import os

from pathlib import Path
from typing import Iterator

from fai_backend.files.document_loaders import IBaseLoader
from fai_backend.files.documents import Document
from fai_backend.files.document_loaders.parsers import PyPDFParser
from fai_backend.files.document_loaders.blob import Blob


class IBasePDFLoader(IBaseLoader):
    def __init__(self, file_path: str | Path):
        self.file_path = str(file_path)
        if "~" in self.file_path:
            self.file_path = os.path.expanduser(self.file_path)

        if not os.path.isfile(self.file_path):
            raise ValueError("File path %s is not a valid file" % self.file_path)

    @property
    def source(self) -> str:
        return self.file_path


class PyPDFLoader(IBasePDFLoader):
    def __init__(self, file_path: str, extract_images: bool = False) -> None:
        try:
            import pypdf
        except ImportError:
            raise ImportError('pypdf package not found, please install it with `pip install pypdf`')
        super().__init__(file_path)
        self.parser = PyPDFParser(extract_images=extract_images)

    def lazy_load(self) -> Iterator[Document]:
        blob = Blob.from_path(self.file_path)
        yield from self.parser.parse(blob)
