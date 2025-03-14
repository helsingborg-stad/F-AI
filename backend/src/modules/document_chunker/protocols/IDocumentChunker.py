from typing import Protocol

from src.modules.document_chunker.models.Chunk import Chunk


class IDocumentChunker(Protocol):
    def chunk(self, path_or_url: str) -> list[Chunk]:
        ...
