# -*- coding: utf-8 -*-
from pony.orm import *
import configparser
from ej import exceptions

db = Database()

class Problem(db.Entity):
    title = Required(str, unique=True)
    time_limit = Required(int)
    test_cases = Set("TestCase")

    def __repr__(self):
        return f'<Problem[{self.id}]:"{self.title}">'

class TestCase(db.Entity):
    input_ = Required(str, autostrip=False)
    output = Required(str, autostrip=False)
    problem = Required(Problem)

    def __init__(self, **kwargs):
        # Not using pony py_check to customize ValueError message.
        # Validate '\n' as final character in output.
        if kwargs and ('output' in kwargs) and (kwargs['output'][-1] != '\n'):
            raise ValueError('Output not terminated by EOL (\\n).')
        super().__init__(**kwargs)

def init(create_db=True, create_tables=True):
    # TODO create db when doesn't exist
    cfg_file = '/opt/pyej/config.ini'
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    try:
        db.bind('postgres', user=cfg['db']['user'],
                password=cfg['db']['password'], database=cfg['db']['name'])
    except KeyError:
        raise exceptions.ConfigError('Check config file {0}'.format(cfg_file))
    db.generate_mapping(create_tables=create_tables)
