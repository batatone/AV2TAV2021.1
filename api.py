import json

import aiohttp
import asyncio
import time

start_time = time.time()


async def get_pokemon(session, url):
    async with session.get(url) as resp:
        pokemon = await resp.json()
        return pokemon


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 6):
            url = f"http://localhost:3002/api/planosaude?idped={number}"
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        i=0
        for pokemon in original_pokemon:
            print(pokemon[i]['idped'])
            print(pokemon[i]['status'])
            print(pokemon[i]['motivo'])
            print(pokemon[i]['dataped'])
            print(pokemon[i]['datares'])
            i=i+1

#def remove():


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))