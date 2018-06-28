import asyncio
from aiohttp import ClientSession, TCPConnector
from .wordlist import WordlistGenerator
from .utils import print_result_colored, fail_silently, print_started

class Scanner(object):
    def __init__(self, wordlist_path: str, target: str, rate_limit=50):
        self.wordlist_path = wordlist_path
        self.target = target
        self.rate_limit = rate_limit

    @fail_silently
    async def _scan_single(self, bucket: str, session: ClientSession):
        url = f'http://{bucket}.s3.amazonaws.com'

        async with session.get(url) as response:
            await response.read()
            status_code = response.status

            if status_code != 404:
                print_result_colored(f'[+] Found bucket: {url} ({status_code})', status_code)

    @fail_silently
    async def _scan_all(self):
        bucket_gen = WordlistGenerator(self.wordlist_path, self.target)
        connector = TCPConnector(limit=50)
        custom_headers = {
            'User-Agent': 'aiohttp client 0.17'
        }

        async with ClientSession(headers=custom_headers, connector=connector) as session:
            await asyncio.gather(*[
                asyncio.ensure_future(self._scan_single(bucket, session))
                for bucket in bucket_gen
            ])

    @fail_silently
    def run(self):
        print_started(self.target, self.rate_limit)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._scan_all())
        loop.run_until_complete(future)