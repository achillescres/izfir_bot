from pydantic import BaseModel


class TicketAccept(BaseModel):
    user_id: str
    operator_name: str
    chatroom_id: str
    
    class Config:
        orm_mode = True
