from typing import List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType


def _flatten_schema(fields: List[StructType], prefix: str = None) -> List[str]:
    flat = []
    for field in fields:
        name = f"{prefix}.{field.name}" if prefix else field.name
        if type(field.dataType) == StructType:
            flat += _flatten_schema(field.dataType.fields, prefix=name)
        else:
            flat.append(name)
    return flat


def flatten(df: DataFrame) -> DataFrame:
    """
    Flatten dataframe with nested structs and trasform all fields into columns.
    """
    cols_map = [
        (x, x.replace(".", "_").lower())
        for x in _flatten_schema(df.schema.fields)
    ]
    sel_list = [
        F.col(old_col).alias(new_col) for (old_col, new_col) in cols_map
    ]
    df = df.select(*sel_list)
    return df


def to_hive_format(df: DataFrame) -> DataFrame:
    """
    Transform Avro structure into exploded format
    usually ingested into hive tables.
    """
    df = df.select("*", "avro.metadata", "avro.signalData").drop("avro")
    df = df.withColumn("signalData", F.explode("signalData"))

    return flatten(df)
