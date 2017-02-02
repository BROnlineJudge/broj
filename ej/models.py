from pony.orm import *
import configparser

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
    cfg = configparser.ConfigParser()
    cfg.read('/opt/pyej/config.ini')
    db.bind('postgres', user=cfg['db']['user'], password=cfg['db']['password'],
            database=cfg['db']['name'])
    db.generate_mapping(create_tables=create_tables)
