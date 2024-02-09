from collections.abc import Callable
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
