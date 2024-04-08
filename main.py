from utils import headers, url
import aiohttp
import time
import asyncio
import customORM as co
import uploadS3 as us


async def fetch_data(session, url, chain=None, limit=100, next_key=None):
    try:
        # Ensure that the limit does not exceed the maximum allowed value of 100
        limit = min(limit, 100)

        params = {
            "limit": limit,
        }
        if next_key is not None:
            params["next"] = next_key

        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
                return await fetch_data(session, url, chain, limit, next_key)  # Retry the request
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
            # results = []
            count = 0

            while True:
                count += 1
                data = await fetch_data(session, url, chain="ethereum", limit=100, next_key=next_key)
                print(len(data))
                if data is None:
                    break
                if "next" in data:
                    next_key = data["next"]
                else:
                    next_key = None

                co.upload_data(data)
                filename = str(count) + '.json'
                await us.uploadS3(data, filename)

                # results = []
                # Calculate delay based on rate limit (4 requests per second)
                rate_limit = 4  # requests per second
                delay = 1 / rate_limit  # calculate delay in seconds

                # Introduce a delay between requests to avoid hitting rate limits
                await asyncio.sleep(delay)  # Adjust the delay as per API rate limits
    except Exception as e:
        print(f"An error occurred: {e}")


async def main():
    await run_async()


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"All the data is loaded in {end - start} seconds")
