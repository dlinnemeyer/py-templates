# kudos to https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
# for an excellent tutorial on asyncio in python
import asyncio
from aiohttp import web, ClientSession
from random import randint

async def fetch(url, session):
    async with session.get(url) as response:
        print("fetching {}".format(url))
        contents = await response.read()
        print("got {}".format(url))
        sleep_time = randint(1, 4)
        await asyncio.sleep(sleep_time)
        print("handing back {} time {}".format(url, sleep_time))
        return (url, response.status, contents[0:30])


URLS = [
    'http://google.com',
    'http://yahoo.com',
    'http://facebook.com',
    'http://craigslist.com',
    'http://stackoverflow.com'
]


async def run(urls):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        
        return await asyncio.gather(*tasks)


async def hello(request):
    responses = await run(URLS)
    response = web.Response(body=str(responses))
    return response


app = web.Application()
app.router.add_route("GET", "/", hello)
web.run_app(app, host='127.0.0.1', port=8080)
