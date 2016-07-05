import pandas as pd
from sqlalchemy import create_engine

def _construct_postgres_engine(auth_dict):
    return create_engine('postgresql://%s:%s@%s:%d/%s' % (
        auth_dict['username'],
        auth_dict['password'],
        auth_dict['host'],
        auth_dict['port'],
        auth_dict['database']
    ))

def push_dataframe_to_postgres(df, auth_dict, table_name, schema=None, if_exists='replace', chunksize=None):
    df.to_sql(
            table_name,
            _construct_postgres_engine(auth_dict),
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize
    )

def read_dataframe_from_postgres(query, auth_dict, chunksize=None):
    return pd.read_sql(query, _construct_postgres_engine(auth_dict), chunksize=chunksize)
