import asyncio
import json
import os
import shutil
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
                 queue_dir: str = "./_document_queue"
                 ):
        self._callbacks: List[DocumentCallbackType] = []
        self._chunker_factory = chunker_factory
        self._vector_service = vector_service
        self._queue_dir = queue_dir
        self._staging_dir = os.path.join(queue_dir, "staging")

        if not os.path.exists(self._staging_dir):
            os.makedirs(self._staging_dir)

    def get_queue_dir(self) -> str:
        return self._queue_dir

    def get_staging_dir(self) -> str:
        return self._staging_dir

    async def add_to_queue(self, document_filename_or_url: str, meta: DocumentMeta):
        print(f"DocumentQueue adding {document_filename_or_url}")

        is_url_document = is_url(document_filename_or_url)

        ext = os.path.splitext(document_filename_or_url)[1] if not is_url_document else '.url'
        filename = self._generate_unique_filename() + ext
        filepath = os.path.join(self._queue_dir, filename)

        with open(filepath, 'wb') as f:
            if is_url_document:
                f.write(document_filename_or_url.encode())
            else:
                with open(document_filename_or_url, 'rb') as source:
                    f.write(source.read())

        meta_filename = filename + '.meta'
        meta_filepath = os.path.join(self._queue_dir, meta_filename)

        with open(meta_filepath, 'w') as f:
            data_to_write = json.dumps(meta.model_dump())
            f.write(data_to_write)

    async def run_queue_loop(self, stop_event: threading.Event):
        print(f"starting document queue loop in process {os.getpid()}")

        while True:
            try:
                await self.try_process_next_document()

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

    async def try_process_next_document(self) -> bool:
        meta_file = next((f for f in os.listdir(self._queue_dir) if f.endswith('.meta')), None)

        if not meta_file:
            return False

        full_meta_path = os.path.join(self._queue_dir, meta_file)
        real_filename = meta_file[0:-5]
        full_file_path = os.path.join(self._queue_dir, real_filename)

        new_meta_path = os.path.join(self._staging_dir, meta_file)
        new_file_path = os.path.join(self._staging_dir, real_filename)

        space_id: str | None = None
        document_id: str | None = None

        try:
            print(f"DocumentQueue processing {meta_file}")

            shutil.move(full_meta_path, new_meta_path)
            print(f"DocumentQueue moving {full_meta_path} to {new_meta_path}")
            shutil.move(full_file_path, new_file_path)
            print(f"DocumentQueue moving {full_file_path} to {new_file_path}")

            metadata: DocumentMeta
            with open(new_meta_path, 'r') as f:
                metadata = DocumentMeta(**json.load(f))

            space_id = metadata.space_id
            document_id = metadata.document_id

            await self._call_callbacks(
                DocumentStateUpdate(space_id=space_id, document_id=document_id, status='processing'))

            chunker = self._chunker_factory.get(new_file_path)
            chunks = chunker.chunk(new_file_path, name=metadata.source_name)

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
            self._remove_ignore_missing(full_meta_path)
            self._remove_ignore_missing(full_file_path)
            self._remove_ignore_missing(new_meta_path)
            self._remove_ignore_missing(new_file_path)
            print(f"DocumentQueue removed {real_filename} + metadata")

        return True

    @staticmethod
    def _remove_ignore_missing(path):
        try:
            print(f"removing {path}...")
            os.remove(path)
        except FileNotFoundError:
            print(f"removing file not found: {path}")
            pass

    async def _call_callbacks(self, document_state_update: DocumentStateUpdate):
        for callback in self._callbacks:
            await callback(document_state_update)

    @staticmethod
    def _generate_unique_filename():
        return str(uuid4())
