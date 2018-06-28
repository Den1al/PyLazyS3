# PyLazyS3

## About
A Python port of the original [lazys3](https://github.com/nahamsec/lazyrecon) tool to enumerate AWS S3 buckets using different permutations, originally created by [@NahamSec](https://github.com/nahamsec). It utilizes the `asyncio` and `aiohttp` libraries to handle multiple high concurrency requests with great efficiency. 

## Installation
After cloning the repository and navigating to the created folder, simply run:
```bash
pip install -r requirements.txt
```

## Usage
```bash
den1al@lab:~/Python/PyLazyS3| ⟪🐍  lazys3-env⟫ master
⇒  python lazys3.py --help

  _____       _                      _____ ____
 |  __ \     | |                    / ____|___ \
 | |__) |   _| |     __ _ _____   _| (___   __) |
 |  ___/ | | | |    / _` |_  / | | |\___ \ |__ <
 | |   | |_| | |___| (_| |/ /| |_| |____) |___) |
 |_|    \__, |______\__,_/___|\__, |_____/|____/
         __/ |                 __/ |
        |___/ @Daniel_Abeles |___/

usage: lazys3.py [-h] [-p PREFIXES] [-l LIMIT] [-u USER_AGENT] target

Bruteforce AWS s3 buckets using different permutations

positional arguments:
  target                which target to scan

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIXES, --prefixes PREFIXES
                        prefixes file to use (default:
                        lists/common_bucket_prefixes.txt)
  -l LIMIT, --limit LIMIT
                        rate limit the http requests (default: 100)
  -u USER_AGENT, --user-agent USER_AGENT
                        which user agent to use when sending requests
                        (default: aiohttp client 0.17)
```

## Feature Requests
Any feature requests are more then welcome, please create an issue containing all relevant information.

## Credits
* [@NahamSec](http://twitter.com/nahamsec)
* [@JobertAbma](http://twitter.com/JobertAbma)



