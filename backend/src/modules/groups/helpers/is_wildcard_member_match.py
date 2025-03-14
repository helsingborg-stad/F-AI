import re


def is_wildcard_member_match(member_id: str, wildcard_pattern: str) -> bool:
    if '*' not in wildcard_pattern or '@' not in member_id or '@' not in wildcard_pattern:
        return False

    def pattern_to_regex(pattern: str):
        if pattern == '*':
            return re.compile('.+')
        return re.compile(re.escape(pattern))

    member_local, member_domain = member_id.split('@')
    pattern_local, pattern_domain = wildcard_pattern.split('@')

    local_regex = pattern_to_regex(pattern_local)
    domain_regex = pattern_to_regex(pattern_domain)

    is_local_match = local_regex.match(member_local) is not None
    is_domain_match = domain_regex.match(member_domain) is not None

    return is_local_match and is_domain_match
