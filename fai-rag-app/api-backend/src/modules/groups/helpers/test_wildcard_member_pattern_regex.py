import re

import pytest

from src.modules.groups.helpers.wildcard_member_pattern_regex import wildcard_member_pattern_regex


@pytest.mark.parametrize("pattern, should_match", [
    ('*@example.com', True),
    ('*@helsingborg.se', True),
    ('*@some-url.some-ext', True),
    ('asd*@helsingborg.se', False),
    ('*asd@helsingborg.se', False),
    ('**@example.com', False),
    ('john.smith@example.com', False),
    ('real-email@helsingborg.se', False),
    ('*', False),
    ('*@', False),
    ('*@example', False),
    ('*@example.', False),
    ('a@example.com', False),
    ('@example.com', False),
])
def test_wildcard_member_pattern_regex(pattern, should_match):
    result = wildcard_member_pattern_regex.match(pattern)
    assert result is not None if should_match else result is None
