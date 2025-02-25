from urllib.parse import urlparse


def is_url(path_or_url: str) -> bool:
    parsed = urlparse(path_or_url)
    return parsed.scheme in ['http', 'https']
