import ujson
from aiohttp import ClientSession, ClientConnectionError


URL = 'http://127.0.0.1:8000/api/fromBot/message/'


async def _send_message_with_session(session: ClientSession, data):
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    for i in range(3):
        async with session.post(URL, json=data, headers=headers) as resp:
            if (await resp.json()) == 'ok':
                return True

    return False


async def produce_message(user_id, operator_id, message):
    try:
        async with ClientSession(json_serialize=ujson.dumps) as session:
            data = {
                "message": message,
                "user_id": user_id,
                "operator_id": operator_id
            }
            sent = await _send_message_with_session(session, data)
            await session.close()

            if not sent:
                print('Failed to send message to operator')
                return 'err'

            return True

    except ClientConnectionError:
        print('Unable to post message')
        return 'err'
