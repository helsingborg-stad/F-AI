from fai_llm.worker.model import WorkerMessages
from fai_llm.ws.model import WsMessages


class WorkerToWsMessagesAdapter:
    @staticmethod
    def convert_update(in_data: WorkerMessages.JobUpdate):
        return WsMessages.JobUpdateResponse(
            job_id=in_data.job_id,
            message=in_data.message
        )

    @staticmethod
    def convert_done(in_data: WorkerMessages.JobDone):
        return WsMessages.JobDoneResponse(
            job_id=in_data.job_id
        )

    @staticmethod
    def convert_error(in_data: WorkerMessages.JobError):
        return WsMessages.JobFailedResponse(
            job_id=in_data.job_id,
            message=in_data.error
        )

    @staticmethod
    def to_ws(message: WorkerMessages.Base) -> WsMessages.Base:
        converters = {
            'update': WorkerToWsMessagesAdapter.convert_update,
            'done': WorkerToWsMessagesAdapter.convert_done,
            'error': WorkerToWsMessagesAdapter.convert_error
        }

        return converters[message.type](message)
