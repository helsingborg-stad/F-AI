import json
import logging
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse


class APIRouter(APIRoute):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('rich')
        super().__init__(*args, **kwargs)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            response = await original_route_handler(request)

            if isinstance(response, StreamingResponse):
                return await self.handle_streaming_response(request, response)
            else:
                try:
                    self.logger.debug(
                        f'👋 Request: {json.loads(req_body.decode("utf-8")) if req_body else str(req_body)}'
                    )
                except Exception as e:
                    self.logger.debug(e)
                # Log the regular response
                response.background = BackgroundTask(
                    self.logger.debug,
                    f'🫴 Response: {response.body.decode("utf-8")}',
                )

                return response

        return custom_route_handler

    async def handle_streaming_response(
            self, request: Request, response: StreamingResponse
    ) -> Response:
        async def log_streaming_response(response_body: bytes):
            # This function will log the streaming response
            self.logger.info(f'Streaming Response: {response_body.decode("utf-8")}')

        # Create a background task for logging the streaming response
        task = BackgroundTask(log_streaming_response, response_body=b'')
        return StreamingResponse(
            content=response.body_iterator,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task,
        )
