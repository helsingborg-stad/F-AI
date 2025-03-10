import pytest

from src.modules.groups.helpers.is_wildcard_member_match import is_wildcard_member_match


@pytest.mark.parametrize('member_id, pattern, expected', [
    ('john.smith@example.com', '*@example.com', True),
    ('anyone@example.com', '*@example.com', True),
    ('john.smith@helsingborg.se', '*@helsingborg.se', True),
    ('john.smith@example.com', 'john.smith@*', True),
    ('anyone@anywhere.ext', '*@*', True),
    ('jane.doe@example.com', 'john.smith@*', False),
    ('john.smith@example.com', 'jane.doe@*', False),
    ('john.smith@example.se', '*@example.com', False),
    ('john.smith@example', '*@example.com', False),
    ('john.smith@example.com', 'invalid pattern', False),
    ('invalid member', '*@example.com', False),
    ('', '*@example.com', False),
    ('', '', False),
    ('fai-someapikey', '*@*', False)
])
def test_is_wildcard_member_match(member_id, pattern, expected):
    assert is_wildcard_member_match(member_id, pattern) == expected
