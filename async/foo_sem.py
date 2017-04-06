# kudos to https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
# for an excellent tutorial on asyncio in python

import asyncio
from aiohttp import ClientSession
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


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session)


URLS = [
    'http://google.com',
    'http://yahoo.com',
    'http://facebook.com',
    'http://craigslist.com',
    'http://stackoverflow.com'
]


async def run(urls):
    sem = asyncio.Semaphore(2)
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        # responses = await asyncio.gather(*[
        #     asyncio.ensure_future(fetch(url, session))
        #     for url in urls
        # ])
        print_responses(responses)


def print_responses(responses):
    print(responses)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(URLS))
loop.run_until_complete(future)
