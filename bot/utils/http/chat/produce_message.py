import logging

from aiohttp import ClientSession

from bot.utils.http.requests import post
from data.config import SERVER_API


URL = f'{SERVER_API}/fromBot/message/'
response_error = 'err'


async def _send_message_with_session(session: ClientSession, data: dict):
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    for i in range(3):
        async with session.post(URL, json=data, headers=headers) as res:
            if (await res.json()) == 'ok':
                return True

    return False


async def produce_message(user_id, operator_id, message):
    try:
        data = {
            "message": message,
            "user_id": user_id,
            "operator_id": operator_id
        }
        sent = await post(URL, data)

        if not sent:
            logging.info('Failed to send message to operator')
            return response_error

        return 'ok'
    except:
        return response_error
