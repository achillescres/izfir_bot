from bot.utils.http.requests import get, post
from data.config import SERVER_API


response_error = 'err'
URL = f"{SERVER_API}/sendTicket"


async def send_ticket(client_id: str, qu_text: str, faculty: str):
    data = {
        "client_id": client_id,
        "message": qu_text,
        "faculty": faculty
    }
    res = (await post(URL, data)).strip('"')
    if res in ['err']:
        return response_error
    
    return res
