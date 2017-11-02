import pprint
from sqlalchemy import *
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement, _literal_as_text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased


class Explain(Executable, ClauseElement):
    def __init__(self, stmt, analyze=False):
        self.statement = _literal_as_text(stmt)
        self.analyze = analyze


@compiles(Explain, 'postgresql')
def pg_explain(element, compiler, **kw):
    text = "EXPLAIN "
    if element.analyze:
        text += "ANALYZE "
        text += compiler.process(element.statement)
    return text
