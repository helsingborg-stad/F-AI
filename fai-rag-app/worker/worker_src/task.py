from worker_src.providers import TaskType, create_client


def external_api_call(**kwargs) -> None:
    task_id = kwargs.pop("task_id", "N/A")
    client = create_client(TaskType.EXTERNAL_API_CALL)
    status_code = client(**kwargs).execute_task(task_id)

    print(f"Task executed with status code: {status_code}")
