#!/usr/bin/env python
import pika
import sys
import argparse
import logging
import os
import zlib
import json
from ej import consts


def target_judge():
    return "server1"

def problem_type():
    return "programming"

def main():
    '''
    '''
    parser = argparse.ArgumentParser(description='pyej client')
    parser.add_argument('-l', '--language', dest='language',
                        help='TODO lang help',
                        choices=consts.language_names,
                        default=consts.language_names[0])
    parser.add_argument('-f', '--file', help='TODO file help', required=True)
    parser.add_argument('-u', '--user', help='TODO user help', required=True)
    parser.add_argument('-p', '--problem', help='TODO problem help', type=int,
                        required=True)
    parser.add_argument('--log', dest='log_level',help='TODO log help',
                        default='WARN')
    args = parser.parse_args()
    print(args)

    if args.log_level:
        numeric_level = getattr(logging, args.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log_level)
        logging.basicConfig(level=numeric_level,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')

    if os.path.getsize(args.file) > 2621440:
        logging.warn('Maximum file size is 2.5mb.')
        sys.exit(1)

    hostname = 'localhost'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hostname))
    channel = connection.channel()
    channel.exchange_declare(exchange=consts.judge_exchange, exchange_type='topic')

    with open(args.file, 'r') as code_file:
        code = code_file.read()
        language_ext = consts.languages[args.language]
        message_json = json.dumps({'language': language_ext, 'code': code,
                                   'problem': args.problem, 'user': args.user})
        message = zlib.compress(message_json.encode())
        routing_key = target_judge() + '.' + problem_type() + '.' + language_ext
        channel.basic_publish(exchange=consts.judge_exchange,
                              routing_key=routing_key, body=message)
        print(f'[x] Sent {args.language}:\n{code}')

    connection.close()

if __name__ == '__main__':
    main()
