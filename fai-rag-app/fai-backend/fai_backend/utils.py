from collections.abc import Callable
from datetime import datetime, timezone
from typing import TypeVar

T = TypeVar('T')


def try_get_first_match(objects: list[T], condition: Callable[[T], bool]) -> T | None:
    """
    Finds the first object in a list that matches a given condition.

    Parameters:
    - objects: List[T], a list of objects of any type.
    - condition: Callable[[T], bool], a function that takes an object of type T and returns a bool.

    Returns:
    - Optional[T]: The first object that matches the condition, or None if no match is found.
    """
    for obj in objects:
        if condition(obj):
            return obj
    return None


def get_iso_timestamp_now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def format_datetime_human_readable(
        specified_datetime: datetime,
        threshold_days: int = 3,
        format: str = '%B %d, %Y'
):
    """
    Converts a datetime to a human-readable format based on the specified criteria.

    Args:
    - specified_datetime: The datetime to convert.
    - threshold_days: The threshold in days for showing just the date.

    Returns:
    A string representing the time difference in a human-readable format or just the date.
    """
    now = datetime.now()
    difference = now - specified_datetime
    days = difference.days
    hours, remainder = divmod(difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > threshold_days:
        return specified_datetime.strftime(format)
    elif days == 1 or (
            days < 1 and hours > 23):  # Adjusting for edge case where difference is just under 24 hours but on 'yesterday'
        return 'Yesterday'
    elif days > 1:
        return f'{days} days ago'
    elif hours >= 1:
        return f'{hours} hours ago'
    else:
        return f'{minutes} minutes ago'
