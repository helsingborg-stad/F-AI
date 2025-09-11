from datetime import datetime
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.models.models.Model import Model


class MongoModelService:
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def get_available_models(self, as_uid: str) -> list[Model]:
        cursor = self._database['chat_models'].find()
        return [self._doc_to_model(doc) async for doc in cursor]

    async def set_available_models(self, models: list[Model]) -> bool:
        await self._database['chat_models'].drop()
        if len(models) == 0:
            return True
        result = await self._database['chat_models'].insert_many([
            {
                'key': model.key,
                'provider': model.provider,
                'display_name': model.display_name,
                'description': model.description,
                'meta': model.meta,
                'created_at': model.created_at,
                'updated_at': model.updated_at,
                'status': model.status,
                'visibility': model.visibility,
                'version': model.version
            } for model in models
        ])
        return result.acknowledged

    async def create_model(self, model: Model, as_uid: str) -> bool:
        """Create a new model with validation and lifecycle fields."""
        try:
            existing = await self._database['chat_models'].find_one({'key': model.key})
            if existing:
                return False

            model_dict = {
                'key': model.key,
                'provider': model.provider,
                'display_name': model.display_name,
                'description': model.description,
                'meta': model.meta,
                'created_at': model.created_at,
                'updated_at': model.updated_at,
                'status': model.status,
                'visibility': model.visibility,
                'version': model.version
            }

            result = await self._database['chat_models'].insert_one(model_dict)
            return result.acknowledged
        except Exception:
            return False

    async def get_model(self, key: str, as_uid: str) -> Model | None:
        """Get a specific model by key."""
        doc = await self._database['chat_models'].find_one({'key': key})
        if not doc:
            return None

        return self._doc_to_model(doc)

    async def update_model(self, key: str, model: Model, as_uid: str) -> bool:
        """Update an existing model with optimistic locking."""
        try:
            existing = await self._database['chat_models'].find_one({'key': key})
            if not existing:
                return False

            if existing.get('version', 1) != model.version:
                return False

            update_dict = {
                'provider': model.provider,
                'display_name': model.display_name,
                'description': model.description,
                'meta': model.meta,
                'updated_at': datetime.utcnow(),
                'status': model.status,
                'visibility': model.visibility,
                'version': model.version + 1
            }

            result = await self._database['chat_models'].update_one(
                {'key': key},
                {'$set': update_dict}
            )
            return result.modified_count == 1
        except Exception:
            return False

    async def delete_model(self, key: str, as_uid: str) -> bool:
        """Delete a model with dependency validation."""
        try:
            model = await self._database['chat_models'].find_one({'key': key})
            if not model:
                return False

            assistant_count = await self._database['assistants'].count_documents({'model': key})
            if assistant_count > 0:
                return False

            result = await self._database['chat_models'].delete_one({'key': key})
            return result.deleted_count == 1
        except Exception:
            return False

    @staticmethod
    def _doc_to_model(doc) -> Model:
        return Model(
            key=doc['key'],
            provider=doc['provider'],
            display_name=doc['display_name'],
            description=doc.get('description'),
            meta=doc.get('meta', {}),
            created_at=doc.get('created_at', datetime.utcnow()),
            updated_at=doc.get('updated_at', datetime.utcnow()),
            status=doc.get('status', 'active'),
            visibility=doc.get('visibility', 'public'),
            version=doc.get('version', 1)
        )
