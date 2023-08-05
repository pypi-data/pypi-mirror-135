import re

from pandas import DataFrame

MYSQL_TO_PANDAS_OPERATORS = {
    'ALL': 'all',
    'AND': 'and',
    'ANY': 'any',
    'BETWEEN': 'between',
    'EXISTS': 'exists',
    'IN': 'in',
    'LIKE': 'like',
    'NOT': ' not ',
    'OR': 'or',
    'SOME': 'some',
    '=': ' == '
}

def assert_required_columns(df: DataFrame, *required):
    _missing = [col for col in required if col not in df]

    if _missing:
        raise KeyError(*_missing)

# TODO improve by splitting query and handling each literal
def parse_mysql_to_pandas_query(query: str):
    _query = query
    
    for mysql_op, pandas_op in MYSQL_TO_PANDAS_OPERATORS.items():
        _query = _query.replace(mysql_op, pandas_op)
    
    return query
    
    # _query = list(
    #     map(
    #         str.strip,
    #         filter(
    #             None, 
    #             re.split(
    #                 '|'.join([f'(\W{mysql_op})' for mysql_op in MYSQL_TO_PANDAS_OPERATORS.keys()]),
    #                 query
    #             )
    #         )
    #     )
    # )
    