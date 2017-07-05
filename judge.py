#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pony.orm import db_session, sql_debug
from ej import models
from ej import consts
from ej import connection
from ej import compilers
from ej import exceptions
from ej.verdict import Verdict
import pony
import tempfile
import subprocess
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
    parser = argparse.ArgumentParser(description='pyej judge')
    parser.add_argument('-l', '--language', dest='language',
                        help='TODO lang help',
                        choices=consts.languages, required=True)
    parser.add_argument('--log', dest='log_level', help='TODO log help',
                        default='WARNING', choices=consts.log_levels)
    parser.add_argument('--sql', action='store_true', default=True)
    parser.add_argument('--host', help='TODO host help', default='localhost')
    return parser.parse_args()


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
    # TODO lock judge after n JEs?
    if language not in consts.languages:
        logger.warn('unsupported language in get_verdict')
        return Verdict.JE

    try:
        problem = models.Problem.select(lambda p: p.title == problem_id).first()
        if(problem == None):
            return Verdict.JE
    except pony.orm.core.ObjectNotFound:
        logger.warn('pony.orm.core.ObjectNotFound invalid problem id')
        return Verdict.JE
    logger.debug(f'Running {problem!r}')

    with tempfile.TemporaryDirectory() as directory:
        # CODE FILE
        code = code if code else ''
        code_file = open(directory + '/code.' + language, 'w')
        code_file.write(code)
        code_file.close()
        filename = code_file.name

        # COMPILATION
        try:
            executable = compilers.compile(language, directory, filename)
        except exceptions.CompilationError:
            logger.info('compilation error')
            return Verdict.CE
        except (exceptions.JudgeError, exceptions.UnsupportedLanguage):
            logger.error(f'internal error on compilation for {language}')
            return Verdict.JE

        # RUN CODE
        try:
            test_cases = problem.test_cases
            if len(test_cases) < 1:
                logger.error('Problem without test cases on RUN CODE')
                return Verdict.JE

            args = list()
            if(language in consts.runners):
                args.append(consts.runners[language])
            args.append(executable)
            for test_case in test_cases:
                output = subprocess.check_output(args=args,
                                                 timeout=problem.time_limit,
                                                 encoding='utf-8',
                                                 input=test_case.input_)
                if problem.check_code:
                    exec(problem.check_code, globals())
                    try:
                        if not check(test_case.input_,           # noqa: F821
                                     test_case.output, output):
                            return Verdict.WA
                    except:
                        return Verdict.JE
                elif not equal_test_cases(output, test_case.output):
                    logger.info((f'Output [{output!r}] did not match'
                                 f'[{test_case.output!r}]'))

                    if equal_test_cases(output, test_case.output,
                                        normalize=True):
                        return Verdict.PE

                    return Verdict.WA

        except subprocess.TimeoutExpired as tle:
            logger.info(tle)
            return Verdict.TLE
        except subprocess.CalledProcessError as rte:
            logger.info(rte)
            return Verdict.RTE
        except FileNotFoundError as fnfe:
            logger.error(fnfe)
            return Verdict.JE

    return Verdict.AC


def main():
    args = get_parsed_args()
    config_logger(args.log_level)

    # DB
    models.init()
    sql_debug(args.sql)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        logger.info(f'{method.routing_key}')
        msg_from_client = connection.decompress(body)
        verdict = get_verdict(msg_from_client['problem'],
                              msg_from_client['language'],
                              msg_from_client['code'])
        print(f'{verdict!r}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        msg_to_courier = {**msg_from_client, **{'verdict': verdict}}
        with connection.CourierConnection(args.host) as conn:
            conn.send(msg_to_courier)

    with connection.JudgeConnection(args.host, args.language) as conn:
        conn.consume(callback)


if __name__ == '__main__':
    main()
