import re


def try_match_email(email: str, pattern: str) -> bool:
    def pattern_to_regex(p: str) -> str:
        escaped = re.escape(p).replace(r'\*', '.*')
        return f'^{escaped}$'

    if '@' not in pattern:
        raise ValueError('Pattern must contain @')

    pattern_local, pattern_domain = pattern.split('@')
    email_local, email_domain = email.split('@')

    local_regex = pattern_to_regex(pattern_local)
    domain_regex = pattern_to_regex(pattern_domain)

    if re.match(local_regex, email_local) and re.match(domain_regex, email_domain):
        return True

    return False


def test_try_match_email():
    test_cases = [
        ['mr.spex@example.com', '*@*', True],
        ['mr.spex@example.com', '*@example.com', True],
        ['mr.spex@example.com', '*.spex@example.com', True],
        ['mr.spex@example.com', '*.spex@*', True],
        ['mr.spex@example.com', '*.dude@example.com', False],
        ['mr.spex@example.com', '*@other-example.com', False],
        ['mr.spex@example.com', 'mr.spex@other-example.com', False],
        ['mr.spex@example.com', 'mr.spex@*.com', True],
        ['mr.spex@example.com', 'mr.spex@example.*', True],
        ['mr.spex@example.com', 'mr.spex@example', False],
        ['mr.spex@example.com', 'mr.spex@*.*', True],
        ['mr.spex@example.com', 'mr.spex@*', True]
    ]

    for email, pattern, expected in test_cases:
        assert try_match_email(email, pattern) == expected
