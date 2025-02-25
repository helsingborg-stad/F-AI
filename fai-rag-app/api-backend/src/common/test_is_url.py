import pytest

from src.common.is_url import is_url


@pytest.mark.parametrize("url, expected", [
    ('http://example.com', True),
    ('https://www.helsingborg.se/', True),
    ('https://www.example.com/software%20manual.pdf', True),
    ('./dir/file.txt', False),
    ('/home/user/dir/file.txt', False),
])
def test_is_url(url, expected):
    result = is_url(url)
    assert result == expected
