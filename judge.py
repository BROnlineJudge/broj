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
from ej import models
from ej import consts
from ej import connection
from ej.verdict import Verdict


def equal_test_cases(t1, t2, normalize=False):
    if normalize:
        return normalize_presentation(t1) == normalize_presentation(t2)
    else:
        return t1 == t2

def normalize_presentation(s):
    from unidecode import unidecode
    return unidecode(s.strip().casefold())

@db_session
def get_verdict(problem_id, language, code):
    if language not in consts.languages:
        logging.warn('unsupported language in get_verdict')
        return Verdict.JE

    try:
        problem = models.Problem[problem_id]
    except pony.orm.core.ObjectNotFound:
        logging.warn('pony.orm.core.ObjectNotFound invalid problem id')
        return Verdict.JE
    logging.debug(f'Running {problem!r}')

    with tempfile.TemporaryDirectory() as directory:
        # CODE FILE
        code = code if code else ''
        code_file = open(directory + '/code.' + language, 'w')
        code_file.write(code)
        code_file.close()
        filename = code_file.name

        # COMPILATION
        try:
            subprocess.run(args=['g++', filename, '-o', directory + '/prog'],
                           timeout=5, check=True)
        except subprocess.CalledProcessError as cpe:
            logging.info(cpe)
            return Verdict.CE
        except subprocess.TimeoutExpired as tle:
            logging.error(tle)
            return Verdict.JE

        # RUN CODE
        try:
            test_cases = problem.test_cases
            if len(test_cases) < 1:
                logging.error('Problem without test cases on RUN CODE')
                return Verdict.JE

            for test_case in test_cases:
                output = subprocess.check_output(args=[directory + '/prog'],
                                                 timeout=problem.time_limit,
                                                 encoding='utf-8',
                                                 input=test_case.input_)
                if not equal_test_cases(output, test_case.output):
                    logging.info(f'Output [{output!r}] did not match [{test_case.output!r}]')

                    if equal_test_cases(output, test_case.output, True):
                        return Verdict.PE

                    return Verdict.WA

        except subprocess.TimeoutExpired as tle:
            logging.info(tle)
            return Verdict.TLE
        except subprocess.CalledProcessError as rte:
            logging.info(rte)
            return Verdict.RTE
        except FileNotFoundError as fnfe:
            logging.error(fnfe)
            return Verdict.JE

    return Verdict.AC

def main():
    # Args
    parser = argparse.ArgumentParser(description='pyej judge')
    parser.add_argument('-l', '--language', dest='language',
                        help='TODO lang help',
                        choices=consts.languages, required=True)
    parser.add_argument('--log', dest='log_level',help='TODO log help',
                        default='WARN')
    parser.add_argument('--sql', action='store_true', default=True)
    parser.add_argument('--host', help='TODO host help', default='localhost')
    args = parser.parse_args()
    print(args)

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

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        logging.info(f"{method.routing_key}")
        msg_from_client = json.loads(zlib.decompress(body).decode())
        verdict = get_verdict(msg_from_client['problem'],
                              msg_from_client['language'],
                              msg_from_client['code'])
        print(f'{verdict!r}')
        time.sleep(1)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        msg_to_courier = {**msg_from_client, **{'verdict': verdict}}
        # # COURIER
        # connection = pika.BlockingConnection(pika.ConnectionParameters(
        #                                  host='localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue=consts.courier_queue)#, durable=True)
        # channel.basic_publish(exchange='',
        #               routing_key=consts.courier_queue,
        #               body=zlib.compress(json.dumps(msg_to_courier).encode()),
        #               properties=pika.BasicProperties(
        #                  delivery_mode = 2, # make message persistent
        #               ))
        # connection.close()

    with connection.JudgeConnection(args.host, args.language) as conn:
        conn.consume(callback)

if __name__ == '__main__':
    main()
