from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user_id: str
