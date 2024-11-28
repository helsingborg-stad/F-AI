from beanie import Document


class CollectionMetadataModel(Document):
    collection_id: str
    label: str = ''
    description: str = ''
    embedding_model: str | None = ''
    urls: list[str] | None = None

    class Settings:
        name = 'collections'
        use_state_management = True
