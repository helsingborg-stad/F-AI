from typing import Any, Callable, Optional


class Job:
    id: Optional[str] = None


class JobStatus:
    FINISHED = "finished"
    QUEUED = "queued"
    STARTED = "started"
    FAILED = "failed"
    DEFERRED = "deferred"
    CANCELED = "canceled"


class IMessageQueue:
    def enqueue(self, func: Callable[..., Any] | str, *args, **kwargs) -> Job:
        """
        Enqueue a task for background execution.

        :param func: The function to be executed as a background task.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: The created job.
        """
        raise NotImplementedError

    def get_status(self, job_id: str) -> Job:
        """
        Retrieve the status of a specific task.

        :param job_id: The identifier or reference of the task.
        :return: The status of the task.
        """
        raise NotImplementedError

    def get_result(self, job_id: str) -> Optional[Any]:
        """
        Retrieve the result of a completed task.

        :param job_id: The identifier or reference of the task.
        :return: The result of the task if it is completed, or None if the task is not completed.
        """
        raise NotImplementedError
