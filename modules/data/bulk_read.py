from functools import reduce
from pyspark.sql import SparkSession

def get_merged_df(spark: SparkSession, catalog: str, schema: str, substring: str):
    """
    Merges all tables within the specified catalog and schema whose names contain a given substring.
    
    Args:
        spark (SparkSession): The Spark session to use for table operations.
        catalog (str): The catalog name to search tables in.
        schema (str): The schema name to search tables in.
        substring (str): Substring to match table names.

    Returns:
        DataFrame: A single Spark DataFrame containing the union of all matched tables, 
                   allowing for missing columns.
    """
    tables: list = spark.catalog.listTables(f"{catalog}.{schema}")
    trip_tables: list = [table.name for table in tables if substring in table.name]
    dfs: list = []
    for table in trip_tables:
        df = spark.read.table(f"{catalog}.{schema}.{table}")
        dfs.append(df)
    return reduce(lambda df1, df2: df1.unionByName(df2, allowMissingColumns=True), dfs)