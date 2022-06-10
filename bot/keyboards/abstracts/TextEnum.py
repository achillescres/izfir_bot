from enum import Enum


class TextEnum(Enum):
    @classmethod
    def values(cls) -> list:
        return [item.value for item in cls]
