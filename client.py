#!/usr/bin/env python
from ej import connection
from ej import consts
import argparse
import os
import sys

import logging
logger = logging.getLogger(__name__)


def config_logger(level):
    sh = logging.StreamHandler()
    sh.setLevel(level)
    fmt = '%(asctime)s %(levelname)-8s %(name)s %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    sh.setFormatter(logging.Formatter(fmt, datefmt))
    logger.addHandler(sh)


def get_parsed_args():
    parser = argparse.ArgumentParser(description='pyej client')
    parser.add_argument('-l', '--language', dest='language',
                        help='TODO lang help',
                        choices=consts.languages, required=True)
    parser.add_argument('--log', dest='log_level', help='TODO log help',
                        default='INFO', choices=consts.log_levels)
    parser.add_argument('-f', '--file', help='TODO file help', required=True)
    parser.add_argument('-u', '--user', help='TODO user help', required=True)
    parser.add_argument('-p', '--problem', help='TODO problem help', type=int,
                        required=True)
    parser.add_argument('--host', help='TODO host help', default='localhost')
    return parser.parse_args()


def main():
    args = get_parsed_args()
    config_logger(args.log_level)

    if os.path.getsize(args.file) > 2621440:
        logger.warn('Maximum file size is 2.5mb.')
        sys.exit(1)

    with connection.JudgeConnection(args.host, args.language) as conn:
        with open(args.file, 'r') as code_file:
            code = code_file.read()
            message = {'language': args.language,
                       'code': code,
                       'problem': args.problem,
                       'user': args.user}
            conn.send(message)
            print(f'[x] Sent {args.language}:\n{code}')


if __name__ == '__main__':
    main()
