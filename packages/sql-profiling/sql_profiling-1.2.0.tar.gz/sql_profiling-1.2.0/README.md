# [sql-profiling](https://github.com/deschman/SQL_Profiling)

## Description
Automatically profile table by name, source database type, and DSN.

## Examples
### Python Script
    # %% Imports
    # %%% 3rd Party
    import distributed

    # %%% User Defined
    import sql_profiling


    # %% Script
    if __name__ == '__main__':
    # Create distributed client for use by query engine
    client: distributed.Client = distributed.Client()

    # Query database and build data profile
    Profile: sql_profiling.ProfileReport = sql_profiling.profile_data(
        'ODATA_D.VW_FACT_SALES',
        'SailfishDev',
        sample_factor=1000000,
        primary_key='SALES_DETAIL_ID')
    # Output profile to html file for view
    Profile.to_file("FACT_SALES Sample 1M.html", False)

### Command Line Interface
    python -m sql_profiling ODATA_D.VW_FACT_SALES -dsn SailfishDev -sf 1000000 -pk SALES_DETAIL_ID
