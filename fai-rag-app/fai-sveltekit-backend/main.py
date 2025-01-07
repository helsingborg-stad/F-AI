from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/chat/stream/")
async def chat_stream(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    # For now, just echo back the user's message (parrot)
    response_message = f"Echo: {user_message}"
    return {"response": response_message}
