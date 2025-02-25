from unstructured.partition.html import partition_html

from src.common.is_url import is_url
from src.modules.document_chunker.helpers.unstructured_element_to_chunk import unstructured_element_to_chunk
from src.modules.document_chunker.models.Chunk import Chunk
from src.modules.document_chunker.protocols.IDocumentChunker import IDocumentChunker


class HTMLDocumentChunker(IDocumentChunker):
    def chunk(self, path_or_url: str) -> list[Chunk]:
        if is_url(path_or_url):
            elements = partition_html(
                url=path_or_url,
                ssl_verify=True,
                chunking_strategy='basic',
                unique_element_ids=True,
            )
        else:
            elements = partition_html(filename=path_or_url, chunking_strategy='basic', unique_element_ids=True)

        return [unstructured_element_to_chunk(element) for element in elements]
