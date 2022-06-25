from aiohttp import ClientConnectionError

from bot.utils.http.requests import post
from data.config import SERVER_API


URL = f'{SERVER_API}/fromBot/cancelChat/'


async def cancel(operator_id, user_id):
    try:
        data = {
            'operator_id': operator_id,
            'user_id': user_id,
            'message': 'cancelling message',
        }
        
        return await post(URL, data=data)
    except ClientConnectionError:
        return 'err'
