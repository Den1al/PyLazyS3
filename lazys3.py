import asyncio
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from lazys3.scanner import Scanner
from lazys3.utils import banner

def parse_args():
    print(banner())

    parser = ArgumentParser(
        description='Bruteforce AWS s3 buckets using different permutations',
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'target', help='which target to scan')
    parser.add_argument('-p', '--prefixes', help='prefixes file to use',
                        default='common_bucket_prefixes.txt')

    parser.add_argument('-l', '--limit', help='rate limit the http requests', default=100, type=int)

    return parser.parse_args()


def main():
    args = parse_args()

    Scanner(
        wordlist_path=args.prefixes,
        target=args.target,
        rate_limit=args.limit
    ).run()


if __name__ == "__main__":
    main()
