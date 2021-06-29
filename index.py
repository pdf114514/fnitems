from sanic import Sanic
from sanic import response as res
from aiohttp import ClientSession
from asyncio import gather, sleep
import aiofiles

import json
import os
from traceback import format_exc as error

types = [
    'outfit', 'emote',
    'backpack', 'pickaxe',
    'glider', 'loadingscreen',
    'contrail', 'emoji',
    'wrap', 'spray',
    'toy', 'petcarrier',
    'music'
]
subtypes = [
    'banners',
    'avatars',
    'newitems',
    'all'
]

async def mainloop(session: ClientSession):
    while True:
        try:
            print('getting from fortnite-api')
            if not os.path.exists('./json'):
                os.mkdir('json')
            async with session.get('https://fortnite-api.com/cosmetics/br/') as resp:
                data = (await resp.json())['data']
            async with session.get('https://fortnite-api.com/v1/banners') as resp:
                banners = (await resp.json())['data']
            async with session.get('https://benbot.app/api/v1/newCosmetics') as resp:
                _newitems = (await resp.json())['items']
            async with session.get('https://cdn2.unrealengine.com/Kairos/data/avatars.json') as resp:
                _avatars = await resp.json()
            newitems = []
            for item in _newitems:
                newitems.append({
                    'name':item['name'],
                    'description':item['description'],
                    'id':item['id'],
                    'rarity':item['rarity'].lower(),
                    'images':{
                        'icon':{
                            'url':item['icons']['icon']
                        }
                    }
                })
            avatars=[]
            for avatarid in _avatars.keys():
                avatars.append({
                    'name':_avatars[avatarid],
                    'description':'',
                    'id':avatarid,
                    'rarity':'common',
                    'images':{
                        'icon':{
                            'url':f'https://cdn2.unrealengine.com/Kairos/portraits/{avatarid}.png?preview=1'
                        }
                    }
                })
            async def _save(t: str, data: list):
                async with aiofiles.open(f'json/{t}.json', 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(sorted([i for i in data if i["type"] == t], key=lambda x:x['id'], reverse=False), indent='    '))
                print('saved:', t, end='          \r')
            async def _save2(filename: str, data): # :list | dict
                async with aiofiles.open(f'json/{filename}.json', 'w', encoding='utf-8') as f:
                    if isinstance(type(data), list):data.sort()
                    await f.write(json.dumps(sorted(data, key=lambda x:x['id'], reverse=False) if isinstance(type(data), dict) else data, indent='   '))
                print('saved:', filename, end='          \r')
            await gather(*[_save(t, data) for t in types], _save2('all', data), _save2('banners', banners), _save2('newitems', newitems), _save2('avatars', avatars))
            await sleep(600)
        except Exception as e:
            print('Exception in mainloop:', e)
            print(error())
            await sleep(15)
            continue

app = Sanic('Server')
app.static('/static', './static')

@app.listener('after_server_start')
async def listener(app, loop):
    loop.create_task(mainloop(ClientSession()))

@app.route('/')
async def root(req):
    return await res.file('html/root.html')

@app.route('/<t>')
async def t(req, t):
    return await res.file('html/viewer.html')

@app.route('/api')
async def api(req):
    return res.json(types+subtypes)

@app.route('/api/<t>')
async def apit(req, t):
    if not os.path.isfile(f'json/{t}.json'):
        return res.json({'message':'Not Found', 'status':404})
    return await res.file(f'json/{t}.json', mime_type='application/json')

def main():
    app.run('0.0.0.0', 8000)

if __name__ == '__main__':
    main()