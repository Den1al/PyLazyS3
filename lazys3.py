import asyncio
from aiohttp import ClientSession
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def banner():
    return """
  _____       _                      _____ ____  
 |  __ \     | |                    / ____|___ \ 
 | |__) |   _| |     __ _ _____   _| (___   __) |
 |  ___/ | | | |    / _` |_  / | | |\___ \ |__ < 
 | |   | |_| | |___| (_| |/ /| |_| |____) |___) |
 |_|    \__, |______\__,_/___|\__, |_____/|____/ 
         __/ |                 __/ |             
        |___/  @Daniel_Abeles |___/   @NahamSec  
    """


def parse_args():
    parser = ArgumentParser(
        description='',
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-n', '--name', help='which target to scan', required=True)
    parser.add_argument('-p', '--prefixes', help='prefixes file to use',
                        default='common_bucket_prefixes.txt')

    return parser.parse_args()


def fail_silently(func):
    async def _wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            return None
    return _wrapper


class Scanner(object):
    def __init__(self, wordlist_path: str, company_name: str):
        self.wordlist_path = wordlist_path
        self.company_name = company_name

    @fail_silently
    async def _scan_single(self, bucket: str, session: ClientSession):
        url = f'http://{bucket}.s3.amazonaws.com'

        async with session.get(url) as response:
            await response.read()
            status_code = response.status

            if status_code != 404:
                print(f'Found bucket: {url} ({status_code})')

    async def _scan_all(self):
        bucket_gen = WordlistGenerator(self.wordlist_path, self.company_name)
        custom_headers = {
            'User-Agent': 'aiohttp client 0.17'
        }

        async with ClientSession(headers=custom_headers) as session:
            await asyncio.gather(*[
                asyncio.ensure_future(self._scan_single(bucket, session))
                for bucket in bucket_gen
            ])

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self._scan_all())
            loop.run_until_complete(future)
        except KeyboardInterrupt:
            print('Stopping scan...')


class WordlistGenerator(object):

    common_environments = ('dev', 'development', 'stage',
                           's3', 'staging', 'prod', 'production', 'test')

    def __init__(self, wordlist_path: str, company_name: str):
        self.wordlist_path = wordlist_path
        self.company_name = company_name

    def _create_file_gen(self):
        with open(self.wordlist_path, 'r') as f:
            for line in f:
                yield line.strip()

    def _permute_envs(self, prefix: str):
        for env in self.common_environments:
            for fmt in ['%s-%s-%s', '%s-%s.%s', '%s-%s%s', '%s.%s-%s', '%s.%s.%s']:
                yield fmt % (self.company_name, prefix, env)

    def _permute_host(self, prefix: str):
        for fmt in ['%s.%s', '%s-%s', '%s%s']:
            yield fmt % (self.company_name, prefix)
            yield fmt % (prefix, self.company_name)

    def _create_gen(self):
        yield self.company_name

        for prefix in self._create_file_gen():
            yield from self._permute_envs(prefix)
            yield from self._permute_host(prefix)

    def __iter__(self):
        return self._create_gen()


def main():
    print(banner())
    args = parse_args()

    Scanner(
        wordlist_path=args.prefixes,
        company_name=args.name
    ).run()


if __name__ == "__main__":
    main()
