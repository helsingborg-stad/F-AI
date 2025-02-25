from src.modules.document_chunker.DocxDocumentChunker import DocxDocumentChunker
from src.modules.document_chunker.ExcelDocumentChunker import ExcelDocumentChunker
from src.modules.document_chunker.HTMLDocumentChunker import HTMLDocumentChunker
from src.modules.document_chunker.MarkdownDocumentChunker import MarkdownDocumentChunker
from src.modules.document_chunker.PDFDocumentChunker import PDFDocumentChunker
from src.modules.document_chunker.helpers.get_mime_type import get_mime_type
from src.modules.document_chunker.protocols.IDocumentChunker import IDocumentChunker


class DocumentChunkerFactory:
    def __init__(self):
        pass

    def get(self, path_or_url: str) -> IDocumentChunker:
        mime_map: dict[str, type[IDocumentChunker]] = {
            'application/pdf': PDFDocumentChunker,
            'text/plain': MarkdownDocumentChunker,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocxDocumentChunker,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelDocumentChunker,
            'text/html': HTMLDocumentChunker,
        }

        mime_type = get_mime_type(path_or_url)

        if mime_type not in mime_map:
            raise ValueError(f'Mime type {mime_type} not supported')

        return mime_map[mime_type]()
