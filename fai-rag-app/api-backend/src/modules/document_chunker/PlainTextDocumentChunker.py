import requests
from unstructured.partition.text import partition_text

from src.common.is_url import is_url
from src.modules.document_chunker.helpers.unstructured_element_to_chunk import unstructured_element_to_chunk
from src.modules.document_chunker.models.Chunk import Chunk
from src.modules.document_chunker.protocols.IDocumentChunker import IDocumentChunker


class PlainTextDocumentChunker(IDocumentChunker):
    def chunk(self, path_or_url: str) -> list[Chunk]:
        if is_url(path_or_url):
            response = requests.get(path_or_url)
            elements = partition_text(
                text=response.text,
                ssl_verify=True,
                unique_element_ids=True,
            )
            for element in elements:
                element.metadata.url = path_or_url
        else:
            elements = partition_text(filename=path_or_url, unique_element_ids=True)

        return [unstructured_element_to_chunk(element) for element in elements]
