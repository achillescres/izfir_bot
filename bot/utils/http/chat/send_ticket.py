from bot.utils.http.requests import get, post
from data.config import SERVER_API


response_error = 'err'
URL = f"{SERVER_API}/sendTicket"


async def send_ticket(chat_id: str, faculty: str):
    data = {
        chat_id: chat_id,
        faculty: faculty
    }
    res = (await post(f'{URL}/{chat_id}/{faculty}', data)).strip('"')
    if res in 'err':
        return response_error
    
    return res
