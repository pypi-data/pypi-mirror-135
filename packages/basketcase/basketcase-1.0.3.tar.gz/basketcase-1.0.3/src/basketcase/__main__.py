import argparse
import sys
from . import basketcase

def main():
    parser = argparse.ArgumentParser(description='Fetch resources from Instagram.')
    parser.add_argument('-c', '--cookie', help='The session cookie id')
    args = parser.parse_args()

    urls = set()

    for line in sys.stdin:
        line = line.rstrip()

        if (line):
            urls.add(line)

    bc = basketcase.BasketCase(args.cookie)
    bc.fetch(urls)

if __name__ == '__main__':
    main()

