import requests

from worker_src.protocol import APIClient


class ExternalAPIClient:
    def __init__(self, base_url: str, path: str, data=str) -> None:
        self.base_url = base_url
        self.path = path
        self.data = data

    def execute_task(self, task_id: str) -> int:
        url = f"{self.base_url}/{self.path}"
        response = requests.post(url=url, data=[("directory_path", self.data)])
        print(f"Task executed with task id: {task_id}")
        return response.status_code


def create_client(type: str, base_url: str, path: str) -> APIClient:
    if type == "external":
        return ExternalAPIClient(base_url, path)

    raise ValueError("Invalid type")
