import asyncio
import json
import os
import threading
from typing import List
from uuid import uuid4

from src.common.is_url import is_url
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.document_queue.protocols.IDocumentQueueService import IDocumentQueueService, DocumentCallbackType, \
    DocumentStateUpdate
from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.protocols.IVectorService import IVectorService


class LocalFileDocumentQueueService(IDocumentQueueService):
    def __init__(self,
                 chunker_factory: DocumentChunkerFactory,
                 vector_service: IVectorService,
                 ):
        self._callbacks: List[DocumentCallbackType] = []
        self._chunker_factory = chunker_factory
        self._vector_service = vector_service
        self._queue_dir = "_document_queue"

    async def add_to_queue(self, document_filename_or_url: str, meta: DocumentMeta):
        print(f"DocumentQueue adding {document_filename_or_url}")

        is_url_document = is_url(document_filename_or_url)

        ext = os.path.splitext(document_filename_or_url)[1] if not is_url_document else '.url'
        filename = self._generate_unique_filename() + ext
        filepath = os.path.join(self._queue_dir, filename)

        with open(filepath, 'wb') as f:
            data_to_write = document_filename_or_url.encode() if is_url_document else open(document_filename_or_url,
                                                                                           'rb').read()
            f.write(data_to_write)

        meta_filename = filename + '.meta'
        meta_filepath = os.path.join(self._queue_dir, meta_filename)

        with open(meta_filepath, 'w') as f:
            data_to_write = json.dumps(meta.model_dump())
            f.write(data_to_write)

    async def run_queue_loop(self, stop_event: threading.Event):
        print(f"starting document queue loop in process {os.getpid()}")
        if not os.path.exists(self._queue_dir):
            os.makedirs(self._queue_dir)

        while True:
            try:
                meta_files = [f for f in os.listdir(self._queue_dir) if f.endswith('.meta')]

                for meta_file in meta_files:
                    real_filename = meta_file[0:-5]

                    space_id: str | None = None
                    document_id: str | None = None

                    try:
                        print(f"DocumentQueue processing {meta_file}")

                        metadata: DocumentMeta
                        with open(os.path.join(self._queue_dir, meta_file), 'r') as f:
                            metadata = DocumentMeta(**json.load(f))

                        space_id = metadata.space_id
                        document_id = metadata.document_id

                        await self._call_callbacks(
                            DocumentStateUpdate(space_id=space_id, document_id=document_id, status='processing'))

                        full_path = os.path.join(self._queue_dir, real_filename)
                        chunker = self._chunker_factory.get(full_path)
                        chunks = chunker.chunk(full_path, name=metadata.source_name)

                        print(f"DocumentQueue chunking {real_filename} using {chunker}")
                        documents = [VectorDocument(
                            id=chunk.id,
                            content=chunk.content,
                            metadata={
                                'source': chunk.source,
                                'page_number': chunk.page_number or -1
                            }
                        ) for chunk in chunks]

                        print(f"DocumentQueue vectorizing {real_filename}")
                        await self._vector_service.add_documents_to_vector_space(
                            space=space_id,
                            embedding_model=metadata.embedding_model,
                            documents=documents
                        )

                        print(f"DocumentQueue done {real_filename}")

                        await self._call_callbacks(
                            DocumentStateUpdate(space_id=space_id, document_id=document_id, status='ready'))

                    except Exception as e:
                        print(f"Error processing {meta_file}: {e}")

                        if space_id and document_id:
                            await self._call_callbacks(
                                DocumentStateUpdate(space_id=space_id, document_id=document_id, status='error'))
                    finally:
                        os.remove(os.path.join(self._queue_dir, meta_file))
                        os.remove(os.path.join(self._queue_dir, real_filename))
                        print(f"DocumentQueue removed {real_filename} + metadata")

                for _ in range(10):
                    if stop_event.is_set():
                        print("document queue stopping")
                        return
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                print("document queue cancelled")
                break
            except Exception as e:
                print(f"Error in background task: {e}")
                await asyncio.sleep(1)

    def add_document_callback(self, callback: DocumentCallbackType):
        self._callbacks.append(callback)

    async def _call_callbacks(self, document_state_update: DocumentStateUpdate):
        for callback in self._callbacks:
            await callback(document_state_update)

    @staticmethod
    def _generate_unique_filename():
        return str(uuid4())
