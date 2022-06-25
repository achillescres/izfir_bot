import ujson
import websockets


async def produce(sender_id, sender, operator_id, message):
    async with websockets.connect('ws://127.0.0.1:8000/api/chat/' + operator_id) as ws:
        await ws.send(ujson.dumps({'sender_id': sender_id, 'sender': sender, 'message': message}))
        await ws.recv()
