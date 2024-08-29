from beanie import Document


class CollectionMetadataModel(Document):
    collection_id: str
    label: str | None
    description: str | None

    class Settings:
        name = 'collections'
        use_state_management = True
