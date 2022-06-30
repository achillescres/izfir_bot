from bot.utils.http.requests import post
from data.config import SERVER_API


response_error = 'err'
URL = f"{SERVER_API}/sendTicket"


async def send_ticket(*, client_id: str, qu_text: str, faculty: str) -> str:
    data = {
        "message": qu_text,
        "client_id": client_id,
        "faculty": faculty,
    }
    res = (await post(URL, data=data)).strip('"')
    if res in ['null', '']:
        return response_error
    
    return res
