from pathlib import PurePath
from datetime import datetime

from pydantic import BaseModel, ByteSize


class FileInfo(BaseModel):
    file_name: str
    file_size: ByteSize
    path: str
    collection: str
    mime_type: str
    last_modified: datetime
    upload_date: datetime
    created_date: datetime
