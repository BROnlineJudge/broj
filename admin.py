#!/usr/bin/env python
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
            p = models.Problem(title='dia da vovo', time_limit=5)
            models.TestCase(input_='2\n42\n69\n', output='24\n96\n', problem=p)
            models.TestCase(input_='1\n55\n', output='55\n', problem=p)
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
