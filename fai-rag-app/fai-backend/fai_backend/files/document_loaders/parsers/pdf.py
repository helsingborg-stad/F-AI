from abc import ABC, abstractmethod
from typing import Iterator, List

from fai_backend.files.documents import Document
from fai_backend.files.document_loaders.blob import Blob


class BaseBlobParser(ABC):
    @abstractmethod
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        ...

    def parse(self, blob: Blob) -> List[Document]:
        return list(self.lazy_parse(blob))


class PyPDFParser(BaseBlobParser):
    def __init__(self, extract_images: bool = False) -> None:
        self.extract_images = extract_images

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        import pypdf

        with blob.as_bytes_io() as pdf_file_obj:
            pdf_reader = pypdf.PdfReader(pdf_file_obj)
            yield from [
                Document(page_content=page.extract_text(),
                         metadata={'source': blob.source, 'page': page_number})
                for page_number, page in enumerate(pdf_reader.pages)]
