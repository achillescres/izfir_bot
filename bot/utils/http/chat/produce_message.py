from io import BytesIO

from loguru import logger

from bot.utils.http.requests import post
from data.config import SERVER_API


URL = f'{SERVER_API}/fromBot/message/'
response_error = 'err'


async def produce_message(user_id: int, operator_id: str, message: str):
    try:
        data = {
            "message": message,
            "user_id": user_id,
            "operator_id": operator_id,
        }
        sent = await post(URL, data=data)

        if not sent:
            logger.info('Failed to send message to operator')
            return response_error

        return 'ok'
    except Exception as e:
        logger.error(e)
        logger.error('Can\'t produce_message')
        return response_error
