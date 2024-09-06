import requests
import enum
from typing import Type

from worker_src.protocol import APIClient


class TaskType(enum.Enum):
    EXTERNAL_API_CALL = "external"


class ExternalAPIClient:
    def __init__(self, base_url: str, path: str, data: str) -> None:
        self.base_url = base_url
        self.path = path
        self.data = data

    def execute_task(self, task_id: str) -> int:
        url = f"{self.base_url}/{self.path}"
        response = requests.post(url, json=self.data)
        print(f"Task executed with task id: {task_id}")
        return response.status_code


def create_client(client_type: TaskType) -> Type[APIClient]:
    if client_type == TaskType.EXTERNAL_API_CALL:
        return ExternalAPIClient
