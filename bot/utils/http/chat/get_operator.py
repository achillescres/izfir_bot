from bot.utils.http.requests import get


response_error = 'null'


async def get_operator(chat_id: str, faculty: str):
    for i in range(3):
        try:
            return (await get(f'http://127.0.0.1:8000/api/getOperator/{chat_id}/{faculty}')).strip('"')
        except:
            pass

    return response_error
