from fai_backend.auth.security import try_match_email


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
        ['mr.spex@example.com', 'mr.spex@*', True],
        ['*@example.com', 'mr.spex@*', False],
        ['*@example.com', '*@example.com', False],
        ['*@example.com', '*@*', False]
    ]

    for email, pattern, expected in test_cases:
        assert try_match_email(email, pattern) == expected
