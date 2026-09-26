import asyncio, random, json, websockets, requests
from websockets.exceptions import ConnectionClosed
from pyrogram import Client
from urllib.parse import unquote

async def apikey(client):
    try:
        await client.start()
        web=unquote(await client.get_main_web_app('major','major'))
        data=web.split('tgWebAppData=',1)[1].split('&tgWebAppVersion',1)[0]
        await client.stop()
        raw = requests.post('https://major.bot/api/auth/tg/', json={'init_data': data}, headers={
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://major.bot',
            'referer': 'https://major.bot/history',
            'user-agent': 'Mozilla/5.0'})
        if raw.status_code < 400: return (raw.json())["access_token"]            
    except: return None

async def autocatch():
 ids = []; access = await apikey(Client(''))#your telegram session name
 while True:
    try:
        async with websockets.connect("wss://major.bot/api/catch_coin/", origin="https://major.bot", user_agent_header="Mozilla/5.0") as wss:
            await wss.send(message=json.dumps({"token": access}))
            async for data in wss:
                try:
                    msg = json.loads(data)
                    print(msg)
                    event, id, status = msg.get('event', None), msg.get('id', None), msg.get('status', None)
                    if event != 'coin' and id and not status:  await wss.send(json.dumps({"id": id}))
                    elif id: ids.append(id)
                    if random.randint(0,1) == 0 and len(ids) >= 4:
                        for _ in range(random.randint(1, 4)):
                            id = ids.pop()
                            await wss.send(json.dumps({"id": id}))
                    if len(ids) > 10: del ids[:-7]
                except Exception as e: print(e)

    except ConnectionClosed as e: access = await apikey(Client(''))#your telegram session name
    except KeyboardInterrupt: await wss.close(); break
    except Exception as e: print(e)

asyncio.run(autocatch())
