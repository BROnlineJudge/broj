#!/usr/bin/env python
import pika
import sys
import zlib
import time
import tempfile
import subprocess
import argparse
import logging
import re

def language_from_binding_key(binding_key):
    '''
    '''
    return binding_key.split('.')[-1]

def valid_binding_keys(binding_keys):
    '''
    '''
    for binding_key in binding_keys:
        match = re.match(r'(\*|\w{3,15})\.(\*|\w{3,15})\.(\*|\w{3,15})',
                         binding_key)
        if not match:
            return False
    return True

def runner_cpp(directory, filename):
    '''
    '''
    result = {}

    try:
        subprocess.run(args=['g++', filename, '-o', directory + '/prog'],
                       timeout=5, check=True)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        result['verdict'] = 'CE'

    try:
        result['output'] = subprocess.check_output(args=[directory + '/prog'],
                                                   timeout=3)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
        result['verdict'] = 'TLE'
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        result['verdict'] = 'RTE'
    except FileNotFoundError:
        print('FileNotFoundError')

    return result

def main():
    '''
    '''
    parser = argparse.ArgumentParser(description='pyej judge')
    parser.add_argument('-b, --binds', dest='binding_keys', nargs='+',
                        help='TODO bks help')
    parser.add_argument('--log', dest='log_level',help='TODO log help',
                        default='WARN')
    args = parser.parse_args()
    print(args)

    if not valid_binding_keys(args.binding_keys):
        parser.print_usage(sys.stderr)
        sys.exit(1)

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

    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='xch_topic_pyej',
                             exchange_type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for binding_key in args.binding_keys:
        channel.queue_bind(exchange='xch_topic_pyej',
                           queue=queue_name,
                           routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        language = language_from_binding_key(method.routing_key)
        code = zlib.decompress(body)
        print(" [x] {0}, {1}".format(method.routing_key, code))
        with tempfile.TemporaryDirectory() as temp_dir:
            code_file = open(temp_dir + '/code.' + language, 'w')
            code_file.write(code.decode())
            code_file.close()

            code_runner = {
                'cpp': runner_cpp
            }
            logging.debug('Preparing to run code.')
            rc = code_runner[language](temp_dir, code_file.name)
            print(rc)
            logging.debug('Finished running code.')

            while True:
                pass

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
