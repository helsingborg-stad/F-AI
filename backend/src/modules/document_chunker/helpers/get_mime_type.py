import magic
import requests

from src.common.is_url import is_url


def get_mime_type(file_path: str) -> str:
    if is_url(file_path):
        response = requests.head(file_path, allow_redirects=True)
        response.raise_for_status()
        return response.headers['Content-Type'].split(';')[0]
    mime = magic.from_file(file_path, mime=True)

    # Special case since markdown is detected/indistinguishable from plain-text
    if mime == 'text/plain' and file_path.endswith('.md'):
        return 'text/markdown'

    return mime
