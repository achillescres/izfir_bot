from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user_id: str

    class Config:
        orm_mode = True