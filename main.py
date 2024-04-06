from utils import headers, url
import aiohttp
import json
import time
import asyncio
import uploadData as ud
import customORM as co


async def fetch_data(session, url, next_key=None):
    try:
        if next_key is not None:
            url += f"&next={next_key}"
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status}")
                return None
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None


async def run_async():
    try:
        async with aiohttp.ClientSession() as session:
            next_key = None
            results = []
            count = 0

            while True:
                count += 1
                data = await fetch_data(session, url, next_key)
                if data is None:
                    break
                if "next" in data:
                    next_key = data["next"]
                else:
                    next_key = None
                # json_object = json.dumps(data, indent=4)
                results.append(data)
                # result_object = json.dumps(results, indent=2)
                co.upload_data(data)
                filename = str(count) + '.json'
                with open(filename, "w") as outfile:
                    json.dump(results, outfile, indent=2)

                results = []

                # Introduce a delay between requests to avoid hitting rate limits
                await asyncio.sleep(50)  # Adjust the delay as per API rate limits
    except Exception as e:
        print(f"An error occurred: {e}")


async def main():
    await run_async()


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"All the data is loaded in {end - start} seconds")