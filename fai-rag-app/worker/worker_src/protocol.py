from typing import Protocol


class APIClient(Protocol):
    def __init__(self, base_url: str, path: str) -> None:
        ...

    def execute_task(self, task_id: str) -> int:
        ...
