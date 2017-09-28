"""
Converts a reflected database to a JSON spec
"""

from sqlalchemy import inspect
from pprint import pprint, pformat


def map_base(base):
    db_dict = {}
    for table_class in base.classes:
        k, v = map_table(table_class)
        db_dict[k] = v
    return db_dict


def map_table(table_class, generate_num=10):
    tbl = inspect(table_class).tables[0]
    table_dict = {
        'num_generated': generate_num,
        'columns': {}
    }
    for column in tbl.columns:
        k, v = map_column(column)
        table_dict['columns'][k] = v
    return tbl.name, table_dict


def map_column(column):
    c = inspect(column)
    filler, pytype = guess_filler(c)
    return column.name, {
        'type': str(c.type),
        'pytype': pytype,
        'filler': filler,
        'pk': c.primary_key,
        'fk': [str(fk) for fk in c.foreign_keys]
    }


def guess_varchar(inspected):
    return 'random.word', 'str'


def guess_int(inspected):
    return 'random.number', 'int'


def guess_double(inspected):
    return 'random.number', 'float'


def guess_unique(inspected):
    return 'random.uuid', 'str'


def guess_filler(inspected):
    result = (None, None)
    if inspected.primary_key and inspected.server_default:
        pass
    elif inspected.primary_key:
        result = guess_unique(inspected)
    elif inspected.foreign_keys:
        fk = [fk for fk in inspected.foreign_keys][0]
        result = ({
            'column': fk.column.name,
            'table': fk.column.table.name
        }, None)
    else:
        result = {
            'INTEGER': guess_int,
            'VARCHAR': guess_varchar,
            'DOUBLE PRECISION': guess_double
        }[str(inspected.type)](inspected)
    return result
