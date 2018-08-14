# author:   @Daniel_Abeles
# date:     26/06/18 

import os
import asyncio
from aiohttp import ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver
from .wordlist import WordlistGenerator
from .utils import (
    print_result_colored, 
    fail_silently, 
    print_started,
    consume_generator
)


class Scanner(object):
    def __init__(self, wordlist_path: str, target: str, rate_limit, user_agent: str):
        self.wordlist_path = wordlist_path
        self.target = target
        self.rate_limit = rate_limit
        self.user_agent = user_agent

    @fail_silently
    async def _scan_single(self, bucket: str, session: ClientSession):
        url = f'http://{bucket}.s3.amazonaws.com'

        async with session.get(url) as response:
            await response.read()
            status_code = response.status

            if status_code not in (404, 504):
                print_result_colored(f'Found bucket: {url} ({status_code})', status_code)

    @fail_silently
    async def _scan_all(self):
        connection_args = {
            'connector': TCPConnector(limit=self.rate_limit),
            'headers': { 
                'User-Agent': self.user_agent 
            }
        }

        async with ClientSession(**connection_args) as session:
            await asyncio.gather(*[
                asyncio.ensure_future(self._scan_single(bucket, session))
                for bucket in WordlistGenerator(self.wordlist_path, self.target)
            ])

    @fail_silently
    def run(self):
        print_started(self.target, self.rate_limit)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._scan_all())
        loop.run_until_complete(future)