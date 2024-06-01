import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fai_backend.files.document_loaders.parsers.pdf import PyPDFParser

_module_lookup = {
    'PyPDFParser': 'fai_backend.files.document_loaders.parsers.pdf'}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = ['PyPDFParser']
