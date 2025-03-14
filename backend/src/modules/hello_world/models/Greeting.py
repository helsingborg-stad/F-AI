from pydantic import BaseModel


class Greeting(BaseModel):
    language: str
    text: str
