from worker_src.protocol import APIClient
from worker_src.providers import create_client


def external_api_call(api_client_type: str, task_id: str, base_url: str, path: str) -> None:
    api_client: APIClient = create_client(
        type=api_client_type, base_url=base_url, path=path)
    status_code = api_client.execute_task(task_id)
    print(f"Task executed with status code: {status_code}")
