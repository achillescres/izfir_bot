from pydantic import BaseModel


class TicketAccept(BaseModel):
    user_id: str
    chat_room_id: str
    operator_name: str
    
    class Config:
        orm_mode = True
