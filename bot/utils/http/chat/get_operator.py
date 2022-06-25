from bot.utils.http.requests import get
from data.config import SERVER_API


response_error = 'null'
URL = f"{SERVER_API}/getOperator"


async def get_operator(chat_id: str, faculty: str):
    for i in range(3):
        try:
            return (await get(f'{URL}/{chat_id}/{faculty}')).strip('"')
        except:
            pass

    return response_error
