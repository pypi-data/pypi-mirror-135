from pandas import DataFrame

def assert_required_columns(df: DataFrame, *required):
    _missing = [col for col in required if col not in df]

    if _missing:
        raise KeyError(*_missing)

#TODO THIS FUNC WILL PARSE MYSQL QUERY INTO PANDAS
def parse_mysql_to_pandas_query(query: str):
    pass