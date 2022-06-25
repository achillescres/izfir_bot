import ujson
from aiohttp import ClientSession, ClientConnectionError


URL = 'http://127.0.0.1:8000/api/fromBot/cancelChat/'


async def _send_cancel_with_session(session: ClientSession, data):
    for i in range(3):
        async with session.post(URL, json=data) as resp:
            print((await resp.json()).strip())
            if (await resp.json()).strip() == 'ok':
                print('URA   CLOSED')
                return True

    return False


async def cancel(operator_id, user_id):
    try:
        async with ClientSession(json_serialize=ujson.dumps) as session:
            data = {
                'operator_id': operator_id,
                'user_id': user_id,
                'message': 'cancelling message',
            }

            sent = await _send_cancel_with_session(session, data)
            await session.close()

            if not sent:
                print('Failed to cancel chat with operator')
                return 'err'

            return True
    except ClientConnectionError:
        return 'err'
