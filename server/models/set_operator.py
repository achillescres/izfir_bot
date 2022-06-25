from pydantic import BaseModel


class SetOperator(BaseModel):
    user_id: str
    operator_id: str

    class Config:
        orm_mode = True
