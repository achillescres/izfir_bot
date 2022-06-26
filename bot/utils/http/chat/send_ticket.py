from bot.utils.http.requests import post
from data.config import SERVER_API


response_error = 'err'
URL = f"{SERVER_API}/sendTicket"


async def send_ticket(qu_text: str, ticket_id: int, client_id: str, faculty: str):
    data = {
        "message": qu_text,
        "ticket_id": ticket_id,
        "client_id": client_id,
        "faculty": faculty,
    }
    res = (await post(URL, data)).strip('"')
    if res in ['err']:
        return response_error
    
    return res
