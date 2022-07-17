from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    qu: str
    an: str


class Faculty(BaseModel):
    faculty_key: str
    normal_qus_ans: List[Question]

    class Config:
        orm_mode = True


class FacultyOperate(BaseModel):
    faculty_name: str
