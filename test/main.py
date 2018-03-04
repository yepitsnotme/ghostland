import aiohttp
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

gets = ['/',
        '/list',
        '/stats',
        '/chat/main',
        '/chat/main/post',]

def spam():
    for i in range(10**3):
        yield '/'

def full_url(url):
    return 'http://localhost:8080'+url

async def get(session, url):
    async with session.get(url) as res:
        text = await res.read()
        return res

async def get_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get(session, full_url(url))) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

async def main():
    await get_all(spam())
    return

    #results = await get_all(gets)
    #for res in results:
    #    if res.status != 200:
    #        print(res)

asyncio.get_event_loop().run_until_complete(main())
