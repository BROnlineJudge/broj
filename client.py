#!/usr/bin/env python
import pika
import sys
import argparse
import logging
import os
import zlib


g_valid_languages = ['c++', 'c', 'python', 'java', 'ruby']


def target_judge():
    '''
    '''
    return "server1"

def problem_type():
    '''
    '''
    return "programming"

def main():
    '''
    '''
    parser = argparse.ArgumentParser(description='judge code')
    parser.add_argument('-l, --language', dest='language', help='TODO lang help', choices=g_valid_languages, default=g_valid_languages[0])
    parser.add_argument('-f, --file', dest='file', help='TODO file help', required=True)
    parser.add_argument('--log', dest='log_level',help='TODO log help', default='WARN')
    args = parser.parse_args()

    print(args)

    if os.path.getsize(args.file) > 2621440:
        # filesize over 2.5mb
        raise

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

    logging.debug('hey')
    logging.info('hey')
    logging.warn('hey')
    logging.error('hey')
    logging.critical('hey')

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='xch_topic_pyej',
                             exchange_type='topic')

    with open(args.file, 'r') as code:
        message = zlib.compress(code.read().encode())
        routing_key = target_judge() + '.' + problem_type() + '.' + args.language
        channel.basic_publish(exchange='xch_topic_pyej',
                              routing_key=routing_key,
                              body=message)
        print(" [x] Sent %r:%r" % (args.language, message))

    connection.close()


if __name__ == '__main__':
    main()
