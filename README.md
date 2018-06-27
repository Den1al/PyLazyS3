# PyLazyS3

## About
A Python port of the original [lazys3](https://github.com/nahamsec/lazyrecon) script to bruteforce for AWS s3 buckets using different permutations, originally created by [@NahamSec](https://github.com/nahamsec).

## Usage
```bash
den1al@lab:~/Python/PyLazyS3| ⟪🐍  3.6.5⟫ master⚡
⇒  python lazys3.py -h

  _____       _                      _____ ____
 |  __ \     | |                    / ____|___ \
 | |__) |   _| |     __ _ _____   _| (___   __) |
 |  ___/ | | | |    / _` |_  / | | |\___ \ |__ <
 | |   | |_| | |___| (_| |/ /| |_| |____) |___) |
 |_|    \__, |______\__,_/___|\__, |_____/|____/
         __/ |                 __/ |
        |___/  @Daniel_Abeles |___/   @NahamSec

usage: lazys3.py [-h] -n NAME [-p PREFIXES]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  which target to scan (default: None)
  -p PREFIXES, --prefixes PREFIXES
                        prefixes file to use (default:
                        common_bucket_prefixes.txt)
```

## Credits
* [@NahamSec](http://twitter.com/nahamsec)
* [@JobertAbma](http://twitter.com/JobertAbma)



