from enum import Enum


class TextEnum(Enum):
    @classmethod
    def texts(cls) -> list:
        return [item.value for item in cls]
