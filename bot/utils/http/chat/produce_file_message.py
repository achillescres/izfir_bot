from typing import IO

from loguru import logger

from bot.utils.http.requests import post_file
from data.config import SERVER_API


URL = f'{SERVER_API}/fromBot/message/file'
response_error = 'err'


async def produce_file_message(user_id: int, operator_id: str, message: str, file_type: str, file_io: IO):
    try:
        data = {
            # "message": message,
            # "user_id": user_id,
            # "operator_id": operator_id,
            # 'file_type': file_type,
            'file': file_io
        }
        sent = await post_file(URL, data=data)
        
        if not sent:
            logger.info('Failed to send file to operator')
            return response_error
        
        return 'ok'
    except Exception as e:
        logger.error(e)
        logger.error('Can\'t produce_file')
        return response_error
