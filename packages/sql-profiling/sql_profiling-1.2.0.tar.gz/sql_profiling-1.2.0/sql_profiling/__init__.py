# -*- coding: utf-8 -*-
"""Initialize profile module."""


# %% Imports
# %%% Py3 Standard
import os
import urllib
import getpass
import multiprocessing
import math
from typing import List

os.environ['MODIN_ENGINE'] = 'dask'

# %%% 3rd Party
import distributed
import pandas as pd
from modin import pandas as md
from pandas_profiling import ProfileReport


# %% Functions
def _create_db_url(
        dsn: str = 'SailfishProd',
        source_type: str = 'DB2',
        credential_prompt: bool = False) -> str:
    """
    Create sqlalchemy.engine.Engine with given params.

    Parameters
    ----------
    dsn : str, default 'SailfishProd'
        Data Source Name as defined in ODBC connections.
    source_type : str, default 'DB2'
        Database type to be connected to.
    credential_prompt : bool, default False
        If true, user will be prompted to enter username and password.

    Returns
    -------
    str
        Connection to database described by params.
    """

    if credential_prompt:
        db_url: str = (
            f"{source_type.lower()}+pyodbc:///" +
            f"?odbc_connect=DSN={dsn.lower()};UID=" +
            urllib.parse.quote_plus(getpass.getpass('enter username: ')) +
            ";PWD=" +
            urllib.parse.quote_plus(getpass.getpass('enter password: ')))
        print(db_url)
    else:
        db_url: str = (
            f'{source_type}+pyodbc:///?odbc_connect=DSN={dsn}').lower()

    return db_url


# %%% Public
def profile_data(
        table_name: str,
        data_source_name: str = 'SailfishProd',
        source_type: str = 'DB2',
        credential_prompt: bool = False,
        sample_factor: int = 1,
        compress_columns: List[str] = None,
        include_columns: List[str] = None,
        primary_key: List[str] = None) -> ProfileReport:
    """
    Create Pandas Profile and save to HTML.

    Parameters
    ----------
    table_name : str
        Fully qualified table name of table in the format of 'SCHEMA.TABLE'.
    data_source_name : str, default 'SailfishProd'
        Data source name as defined in user ODBC connections.
    source_type : str, default 'DB2'
        Source database type for use in database url.
    credential_prompt : bool, default False
        If True, user will be prompted to input credentials to database.
    sample_factor : int, default 1
        One record per sample_factor will be read for the profile.
    compress_columns : List[str], optional
        List of columns to take out of the profile separated by spaces. All
        other columns will be compressed if this is specified.
    include_columns : List[str], optional
        List of columns to include in the profile separated by spaces. All
        other columns will be excluded from the profile.
    primary_key : str, optional
        Key used to sort data, which may provide a better profile if a data
        sample is being used.

    Returns
    -------
    pandas_profiling.ProfileReport
        Data profile of table.
    """
    url: str = _create_db_url(data_source_name, source_type, credential_prompt)

    if include_columns is not None:
        columns: str = ', '.join(include_columns)
    else:
        # query limit 0 to get all columns
        columns: str = ', '.join(
            pd.read_sql(
                f"""
SELECT *
FROM {table_name}
WHERE
    1 IS NULL
    AND 1 IS NOT NULL""",
                url).columns)

    if compress_columns is not None:
        columns = ', '.join(
            [c for c in columns.split(', ') if c not in compress_columns])

    distinct: str = 'DISTINCT ' if compress_columns is not None else ''

    def get_limit(row_count: int, sample_factor: int, partitions: int) -> int:
        return math.ceil(
            math.ceil(
                row_count /
                sample_factor) /
            partitions)

    partitions: int = multiprocessing.cpu_count()
    if primary_key is not None:
        min_key: int = pd.read_sql(
            f"SELECT MIN({primary_key}) FROM {table_name}",
            url).squeeze()
        max_key: int = pd.read_sql(
            f"SELECT MAX({primary_key}) FROM {table_name}",
            url).squeeze()
        row_count: int = max_key - min_key
        limit: int = get_limit(row_count, sample_factor, partitions)
        page_clause: str = (
            f"WHERE {primary_key} BETWEEN " +
            f"({min_key} + ({sample_factor} * {limit} * {{p}})) AND " +
            f"({min_key} + ({sample_factor} * {limit} * {{p}}) + {limit})")
    else:
        row_count: int = pd.read_sql(
                f"SELECT COUNT(*) FROM {table_name}",
                url).squeeze()
        limit: int = get_limit(row_count, sample_factor, partitions)
        page_clause: str = (
            f"LIMIT {limit} OFFSET ({limit * sample_factor} * {{p}})")

    client: distributed.Client = distributed.default_client()

    futures: distributed.Future = [client.submit(
        pd.read_sql,
        sql=(
            f"SELECT{distinct} {columns} FROM {table_name} " +
            page_clause.format(p=p)),
        con=url
        ) for p in range(partitions)]

    # Watch progress and wait for results
    distributed.progress(futures)

    df: pd.DataFrame = pd.concat(client.gather(futures))

    # de-fragment dataframe
    df = df.copy()

    name_suffix: str = (
        f" including {columns.count(',') + 1} columns"
        if include_columns is not None
        else '')
    name_suffix = (
        name_suffix + f" compressed by {len(compress_columns)} columns"
        if compress_columns is not None
        else '')

    return ProfileReport(
        df,
        title=f"{table_name} Pandas Profile{name_suffix}",
        minimal=True,
        dark_mode=True)
