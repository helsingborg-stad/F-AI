import threading
from collections.abc import Callable
from typing import Protocol, Mapping, Any, Coroutine

from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.document_queue.models.DocumentStateUpdate import DocumentStateUpdate

DocumentCallbackType = Callable[[DocumentStateUpdate], Coroutine[Any, Any, None]]


class IDocumentQueueService(Protocol):
    async def add_to_queue(self, document_filename_or_url: str, meta: DocumentMeta):
        ...

    async def run_queue_loop(self, stop_event: threading.Event):
        ...

    def add_document_callback(self, callback: DocumentCallbackType):
        ...
