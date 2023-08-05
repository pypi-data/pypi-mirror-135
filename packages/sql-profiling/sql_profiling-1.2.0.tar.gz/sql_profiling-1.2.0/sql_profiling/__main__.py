# -*- coding: utf-8 -*-
"""
Automatically profile table by name, source database type, and DSN.

Params
------
table_name : str
    Fully qualified table name of table in the format of 'SCHEMA.TABLE'.
--data_source_name, -dsn : str, default 'SailfishProd'
    Data source name as defined in user ODBC connections.
--source_type, -sf : str, default 'DB2'
    Source database type for use in database url.
--credential_prompt, -cp : str, default False
    If True, user will be prompted to input credentials to database.
--sample_factor, -sf : int, optional
    One record per sample_factor will be read for the profile.
--compress_columns, -cc : str, optional
    List of columns to take out of the profile separated by spaces. All other
    columns will be compressed if this is specified.
--include_columns, -ic : str, optional
    List of columns to include in the profile separated by spaces. All other
    columns will be excluded from the profile.
--primary_key, -pk : str, optional
    Key used to sort data, which may provide a better profile if a data sample
    is being used.
"""


# %% Imports
# %%% Py3 Standard
# import traceback
import os
import argparse
import traceback

# %%% 3rd Party
import distributed
from pandas_profiling import ProfileReport

# %%% User Defined
from sql_profiling import profile_data


# %% Functions
def main() -> None:
    Profile_Argument_Parser: argparse.ArgumentParser = argparse.ArgumentParser(
        'profile.py')
    Profile_Argument_Parser.add_argument(
        'table_name',
        help="Fully qualified name of table in the format of 'SCHEMA.TABLE'")
    Profile_Argument_Parser.add_argument(
        '--data_source_name',
        '-dsn',
        nargs='?',
        default='SailfishProd',
        help="Data source name as defined in user ODBC connections")
    Profile_Argument_Parser.add_argument(
        '--source_type',
        '-s',
        nargs='?',
        default='DB2',
        help="Source database type for use in database url")
    Profile_Argument_Parser.add_argument(
        '--credential_prompt',
        '-cp',
        nargs='?',
        const=True,
        default=False,
        type=bool,
        choices=[True, False],
        help="If True, user will be prompted to input credentials to database")
    Profile_Argument_Parser.add_argument(
        '--sample_factor',
        '-sf',
        type=int,
        default=1,
        help="One record per sample_factor will be read for the profile")
    Profile_Argument_Parser.add_argument(
        '--compress_columns',
        '-cc',
        nargs='*',
        help="If supplied, profile will include unique values in other columns")
    Profile_Argument_Parser.add_argument(
        '--include_columns',
        '-ic',
        nargs='*',
        help="If supplied, profile will include unique values in other columns")
    Profile_Argument_Parser.add_argument(
        '--primary_key',
        '-pk',
        help="Key used to sort data, which may provide a better profile")

    kwargs: dict = vars(Profile_Argument_Parser.parse_args(os.sys.argv[1:]))

    Profile: ProfileReport = profile_data(**kwargs)
    Profile.to_file(
        os.path.join(os.path.dirname(__file__),
                     f"{kwargs.get('table_name')}.html"),
        False)


# %% Script
if __name__ == '__main__':
    try:
        client: distributed.Client = distributed.Client(processes=False)
        main()
    except Exception:
        traceback.print_exc()
    finally:
        input("press enter to close")
