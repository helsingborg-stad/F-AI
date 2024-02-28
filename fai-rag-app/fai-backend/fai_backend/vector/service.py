from typing import Optional, Dict

from fai_backend.vector.interface import IVector
from fai_backend.vector.types import OneOrMany, Embedding


class VectorService:
    vector_db: IVector
    collection_name: str

    def __init__(self, vector_db: IVector, collection_name: str):
        self.vector_db = vector_db
        self.collection_name = collection_name

    @staticmethod
    def _generate_metadata(user_email: str, project_id: str, metadata_version: str = "1.0.0") -> Dict:
        delimiter = "|"

        metadata_tag = (
            f"version:{metadata_version}{delimiter}"
            f"project_id:{project_id}{delimiter}"
            f"user_email:{user_email}"
        )
        return {
            "project_user_id": metadata_tag
        }

    def add_vector_to_project(
            self,
            user_email: str,
            project_id: str,
            ids: OneOrMany[str],
            embeddings: Optional[OneOrMany[Embedding]] = None,
            documents: Optional[OneOrMany[str]] = None,
            uris: Optional[OneOrMany[str]] = None,
    ):
        metadata = self._generate_metadata(user_email, project_id)

        self.vector_db.add(
            collection_name=self.collection_name,
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            uris=uris,
            metadatas=[metadata] * len(ids)
        )

    def query_vector_from_project(
            self,
            user_email: str,
            project_id: str,
            query_texts: Optional[OneOrMany[str]] = None,
            n_results: int = 10,
    ):
        where_filter = self._generate_metadata(user_email, project_id)

        return self.vector_db.query(
            collection_name=self.collection_name,
            query_texts=query_texts,
            n_results=n_results,
            where=where_filter,
        )
