#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from pony.orm import *
from ej import models
from ej import consts


def main():
    # DB
    models.init()
    parser = argparse.ArgumentParser(description='EJ Admin CRUD')

    def create_problem(args):
        print('create')
        print(args)
        with db_session:
            p = models.Problem(title='Dia da Vovó', time_limit=5, check_code="")
            models.TestCase(input_='2\n42\n69\n', output='24\n96\n', problem=p)
            models.TestCase(input_='1\n55\n', output='55\n', problem=p)
            p2 = models.Problem(title='Divide by 2', time_limit=1, 
                                check_code='def check(input, output, user_output):\n    import io\n    inbuf = io.StringIO(input)\n    a = float(inbuf.read())\n    outbuf = io.StringIO(user_output)\n    b = float(outbuf.read())\n    if(abs(a/2.0 - b) < 1e-6):\n        return True\n    return False\n')
            models.TestCase(input_='10\n', output='5\n', problem=p2)
            models.TestCase(input_='11\n', output='5.5\n', problem=p2)
            commit()

    def read_problem(args):
        print('read')
        print(args)
        with db_session:
            print(select(p for p in models.Problem)[:].show())
            print(select(p for p in models.TestCase)[:].show())

    def update_problem(args):
        print('update')
        print(args)

    def delete_problem(args):
        print('delete')
        print(args)
        with db_session:
            delete(p for p in models.Problem)
            delete(p for p in models.TestCase)


    sp = parser.add_subparsers()

    sp_create = sp.add_parser('create')
    sp_create.set_defaults(func=create_problem)

    sp_read = sp.add_parser('read')
    sp_read.set_defaults(func=read_problem)

    sp_update = sp.add_parser('update')
    sp_update.set_defaults(func=update_problem)

    sp_delete = sp.add_parser('delete')
    sp_delete.set_defaults(func=delete_problem)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
