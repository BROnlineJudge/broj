#!/usr/bin/env python
from ej.verdict import Verdict
from ej import consts
from ej import connection
import argparse

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
    parser = argparse.ArgumentParser(description='pyej courier')
    parser.add_argument('--log', dest='log_level',help='TODO log help',
                        default='WARNING', choices=consts.log_levels)
    return parser.parse_args()


def main():
    args = get_parsed_args()
    config_logger(args.log_level)

    def callback(ch, method, properties, body):
        msg_from_judge = connection.decompress(body)
        print(f' [x] Received {msg_from_judge}')
        ch.basic_ack(delivery_tag = method.delivery_tag)

    with connection.CourierConnection('localhost') as conn:
        print('Waiting for messages...')
        conn.consume(callback)


if __name__ == '__main__':
    main()
