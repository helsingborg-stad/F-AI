from __future__ import annotations
import mimetypes
import contextlib
from io import BufferedReader, BytesIO
from pathlib import PurePath
from pydantic import BaseModel, Field
from typing import Any, Dict, Generator


class Blob(BaseModel):
    data: bytes | str | None
    mimetype: str | None = None
    encoding: str = 'utf-8'

    path: str | PurePath | None = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @contextlib.contextmanager
    def as_bytes_io(self) -> Generator[BytesIO | BufferedReader, None, None]:
        if isinstance(self.data, bytes):
            yield BytesIO(self.data)
        elif self.data is None and self.path:
            with open(str(self.path), 'rb') as f:
                yield f
        else:
            raise NotImplementedError(f'Unable to convert blob {self}')

    @classmethod
    def from_path(cls,
                  path: str | PurePath,
                  *,
                  encoding: str = 'utf-8',
                  mime_type: str | None = None,
                  guess_type: bool = True,
                  metadata: Dict | None = None) -> Blob:
        if mime_type is None and guess_type:
            _mimetype = mimetypes.guess_type(path)[0] if guess_type else None
        else:
            _mimetype = mime_type

        return cls(data=None,
                   mimetype=_mimetype,
                   encoding=encoding,
                   path=path,
                   metadata=metadata if metadata is not None else {})
