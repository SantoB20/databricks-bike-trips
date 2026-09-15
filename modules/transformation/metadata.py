from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp

def add_processed_timestamp(df: DataFrame) -> DataFrame:
    """
    Adds processed timestamp audit column to the input DataFrame with the current timestamp.

    Args:
        df (DataFrame): Input Spark DataFrame.

    Returns:
        DataFrame: DataFrame with an additional 'processed_timestamp' column.
    """
    return df.withColumn("processed_timestamp", current_timestamp())