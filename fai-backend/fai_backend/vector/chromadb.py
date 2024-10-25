import chromadb

from fai_backend.vector.base_chromadb import BaseChromaDB


class ChromaDB(BaseChromaDB):
    def __init__(self, db_directory: str):
        super().__init__(
            chromadb.PersistentClient(
                path=db_directory,
                settings=chromadb.Settings(
                    anonymized_telemetry=False,  # opt out of telemetry
                    allow_reset=True
                ),
            ),
        )
