from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/chat/stream/")
async def chat_stream(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    # For now, just echo back the user's message (parrot)
    response_message = f"Echo: {user_message}"
    return {"response": response_message}
