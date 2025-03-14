from unstructured.documents.elements import Element

from src.modules.document_chunker.models.Chunk import Chunk


def unstructured_element_to_chunk(element: Element) -> Chunk:
    return Chunk(
        id=element.id,
        content=element.text,
        source=element.metadata.filename or element.metadata.url,
        page_number=element.metadata.page_number,
    )
