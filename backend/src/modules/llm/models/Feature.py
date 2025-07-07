from enum import Enum, auto


class Feature(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        return name.lower()

    WEB_SEARCH = auto()
    REASONING = auto()
