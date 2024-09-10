from beanie import Document


class CollectionMetadataModel(Document):
    collection_id: str
    label: str = ''
    description: str = ''

    class Settings:
        name = 'collections'
        use_state_management = True
