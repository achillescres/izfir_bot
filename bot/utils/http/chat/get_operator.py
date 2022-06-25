from bot.utils.http.requests import get
from data.config import SERVER_API


response_error = 'err'
URL = f"{SERVER_API}/getOperator"


async def get_operator(chat_id: str, faculty: str):
    res = await get(URL)
    
    if res in ('err', 'null', ''):
        return response_error
    
    return res
