from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from fai_llm.ws.service import WebSocketClient
from fai_llm.ws.starlette_adapter import StarletteConnection

router = APIRouter(
    prefix='/ws',
    tags=['WebSocket']
)


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = WebSocketClient(conn=StarletteConnection(websocket), dc_exc_type=WebSocketDisconnect)
    await client.run()
    # try:
    #     while True:
    #         data = await websocket.receive_text()
    #         await websocket.send_text(f"Message text was: {data}")
    # except WebSocketDisconnect:
    #     print('socket gone')
