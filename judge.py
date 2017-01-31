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
import json

from pony.orm import *
import models
from verdict import Verdict

def language_from_binding_key(binding_key):
    return binding_key.split('.')[-1]

def valid_binding_keys(binding_keys):
    for binding_key in binding_keys:
        match = re.match(r'^(\*|\w{3,15})\.(\*|\w{3,15})\.(\*|\w{3,15})$',
                         binding_key)
        if not match:
            return False
    return True


@db_session
def get_verdict(language, code):
    # compilers = {
    #     'cpp': cpp_compiler
    # }
    # compiled = compilers[language](directory, filename)
    # if not compiled:
    #     return Verdict.CE

    with tempfile.TemporaryDirectory() as directory:
        # CODE FILE
        code_file = open(directory + '/code.' + language, 'w')
        code_file.write(code)
        code_file.close()
        filename = code_file.name

        # COMPILATION
        try:
            subprocess.run(args=['g++', filename, '-o', directory + '/prog'],
                           timeout=5, check=True)
        except subprocess.CalledProcessError:
            logging.error('CalledProcessError on compilation')
            return Verdict.JE
        except subprocess.TimeoutExpired:
            return Verdict.CE

        # RUN CODE
        try:
            problem = models.Problem[1]

            for tc in problem.testcases:
                output = subprocess.check_output(args=[directory + '/prog'],
                                                 timeout=problem.time_limit,
                                                 encoding='utf-8',
                                                 input=tc.input_)
                # assuming always has final endline
                if output != (tc.output + '\n'):
                    return Verdict.WA
        except subprocess.TimeoutExpired:
            return Verdict.TLE
        except subprocess.CalledProcessError:
            return Verdict.RTE
        except FileNotFoundError:
            logging.error('FileNotFoundError on code run')
            return Verdict.JE

    return Verdict.AC

def main():
    # Args
    parser = argparse.ArgumentParser(description='pyej judge')
    parser.add_argument('-b', '--binds', dest='binding_keys', nargs='+',
                        help='TODO bks help', required=True)
    parser.add_argument('--log', dest='log_level',help='TODO log help',
                        default='WARN')
    parser.add_argument('--sql', action='store_true', default=True)
    args = parser.parse_args()
    print(args)


    if not valid_binding_keys(args.binding_keys):
        parser.print_usage(sys.stderr)
        sys.exit(1)

    if args.log_level:
        numeric_level = getattr(logging, args.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {args.log_level}')
        logging.basicConfig(level=numeric_level,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')

    # DB
    models.init()
    sql_debug(args.sql) # TODO working?

    # RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                         host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='xch_topic_pyej', exchange_type='topic')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for binding_key in args.binding_keys:
        channel.queue_bind(exchange='xch_topic_pyej', queue=queue_name,
                           routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        logging.info(f"{method.routing_key}")

        language = language_from_binding_key(method.routing_key)
        code = zlib.decompress(body).decode()
        verdict = get_verdict(language, code)
        print(verdict)
        # # COURIER
        # connection = pika.BlockingConnection(pika.ConnectionParameters(
        #                                  host='localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue='courier')#, durable=True)
        # channel.basic_publish(exchange='',
        #               routing_key='courier',
        #               body=zlib.compress(json.dumps(verdict).encode()),
        #               properties=pika.BasicProperties(
        #                  delivery_mode = 2, # make message persistent
        #               ))
        # connection.close()

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
