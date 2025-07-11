from enum import Enum, auto


class Feature(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        return name.lower()

    WEB_SEARCH = auto()
    REASONING = auto()


def features_from_string(in_str: str) -> list[Feature]:
    if not in_str or len(in_str) == 0:
        return []

    result = []
    for feature_str in in_str.split(','):
        try:
            feature = Feature[feature_str.strip().upper()]
            result.append(feature)
        except KeyError:
            continue

    return result
