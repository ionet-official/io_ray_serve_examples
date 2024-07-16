import aiohttp
import asyncio
import time
import base64
import logging
import backoff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@backoff.on_exception(backoff.expo, aiohttp.client_exceptions.ServerDisconnectedError, max_tries=5)
async def make_request(session, url, data, auth_header): 
    # for now auth_header is not used because endpoint don't have basic auth or any other auth, only cookie
    # don't forget to change cookies to your's
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': '',
    }

    start_time = time.time()
    try:
        async with session.post(url, headers=headers, json=data) as response:
            end_time = time.time()
            elapsed_time = end_time - start_time
            response_text = await response.text()

            print(f"Elapsed time: {elapsed_time:.4f} seconds")
            print(response_text)

            return response_text
            
    except aiohttp.client_exceptions.ServerDisconnectedError as e:
        logger.error(f"Server disconnected error: {e}")
        raise

async def main():
    #change url_id to your's
    url_id = '0f580'
    url = f"https://vscode-{url_id}.tunnels.io.systems/proxy/8000/"

    username = 'IDE_PASSWORD'
    password = 'IDE_PASSWORD'

    auth_str = f"{username}:{password}"
    auth_bytes = auth_str.encode('ascii')
    auth_b64_bytes = base64.b64encode(auth_bytes)
    auth_b64_str = auth_b64_bytes.decode('ascii')
    auth_header = f"Basic {auth_b64_str}"

    
    with open('prompts.txt', 'r', encoding='utf-8') as file:
        data = [line.strip() for line in file.readlines()]

    async with aiohttp.ClientSession() as session:
        for _ in range(3):
            tasks = [make_request(session, url, data[i % len(data)], auth_header) for i in range(5)]  
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
