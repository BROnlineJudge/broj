#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ej import consts
from ej import connection
from ej import verdict
import argparse
import requests

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
    parser.add_argument('--log', dest='log_level', help='TODO log help',
                        default='WARNING', choices=consts.log_levels)
    parser.add_argument('--host', help='TODO host help', default='localhost')
    return parser.parse_args()


def main():
    args = get_parsed_args()
    config_logger(args.log_level)

    def callback(ch, method, properties, body):
        msg_from_judge = connection.decompress(body)
        print(f' [x] Received {msg_from_judge}')
        payload = {'submission' : { 'verdict' : verdict.Verdict(msg_from_judge['verdict']).__str__()}}
        r = requests.patch(msg_from_judge['user'], json=payload)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    with connection.CourierConnection(args.host) as conn:
        print('Waiting for messages...')
        conn.consume(callback)


if __name__ == '__main__':
    main()
