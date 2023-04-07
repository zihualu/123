import asyncio
import aiohttp
import re

async def fetch_emails(session, url):
    async with session.get(url) as response:
        data = await response.json()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(data))
        return emails

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 101):
            url = f'https://jsonplaceholder.typicode.com/posts/{i}/comments'
            tasks.append(asyncio.ensure_future(fetch_emails(session, url)))

        results = await asyncio.gather(*tasks)
        emails = set()
        for res in results:
            for email in res:
                emails.add(email)

        with open('emails.txt', 'w') as f:
            f.write('\n'.join(emails))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    