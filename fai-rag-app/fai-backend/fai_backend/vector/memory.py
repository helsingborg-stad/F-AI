import chromadb

from fai_backend.vector.base_chromadb import BaseVectorDB


class InMemoryVectorDB(BaseVectorDB):
    def __init__(self):
        super().__init__(chromadb.EphemeralClient(
            settings=chromadb.Settings(
                anonymized_telemetry=False,  # opt out of telemetry
                allow_reset=True
            )
        ))
