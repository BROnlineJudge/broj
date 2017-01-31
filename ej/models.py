from pony.orm import *
from ej import config

db = Database()

class Problem(db.Entity):
    title = Required(str, unique=True)
    time_limit = Required(int)
    testcases = Set("TestCase")

class TestCase(db.Entity):
    input_ = Required(str)
    output = Required(str)
    problem = Required(Problem)

def init(create_db=True, create_tables=True):
    db.bind('sqlite', config.DB_PATH + config.DB_NAME, create_db=create_db)
    db.generate_mapping(create_tables=create_tables)
