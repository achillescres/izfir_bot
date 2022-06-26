from pydantic import BaseModel


class TicketAccept(BaseModel):
    user_id: str
    operator_id: str
    ticket_id: str
    answer: str
    
    class Config:
        orm_mode = True
