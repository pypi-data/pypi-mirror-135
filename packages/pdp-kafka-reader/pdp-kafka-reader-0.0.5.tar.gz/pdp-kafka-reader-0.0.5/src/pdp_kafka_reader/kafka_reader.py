import json
from argparse import Namespace
from functools import partial
from typing import Any, Dict, Optional

import fastavro
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.column import Column, _to_java_column
from pyspark.sql.types import StructType

from pdp_kafka_reader.argparser import Command, parse_args
from pdp_kafka_reader.avro_utils import deserialize_avro
from pdp_kafka_reader.transform import to_hive_format


class KafkaReader:
    def __init__(self, spark: SparkSession):
        self._spark = spark

    def read(self, options: Dict[str, Any], topic: Optional[str] = None) -> DataFrame:
        """
        Read data from kafka using kafka options. If you define topic argument,
        it will override `subscribe` option in `options` dictionary.
        """
        if topic:
            options["subscribe"] = topic

        return self._spark.read.format("kafka").options(**options).load()


class KafkaAvroReader(KafkaReader):
    def read_avro(
        self,
        options: Dict[str, Any],
        schema: str,
        topic: Optional[str] = None,
        use_fastavro: bool = True,
    ) -> DataFrame:
        """
        Read messages from kafka and deserialize `value` column into `avro`.
        """
        df = self.read(options, topic)
        if use_fastavro:
            udf_deserialize_avro = self._get_fastavro_udf(schema)
            df = df.withColumn("avro", udf_deserialize_avro(F.col("value"))).drop("value")
        else:
            df = df.withColumn("avro", self._from_avro("value", schema)).drop("value")
        return df

    def _get_fastavro_udf(self, schema: str):
        fastavro_schema = fastavro.parse_schema(json.loads(schema))

        sc = self._spark.sparkContext
        parsed_schema = sc._jvm.org.apache.avro.Schema.Parser().parse(schema)
        java_schema_type = sc._jvm.org.apache.spark.sql.avro.SchemaConverters.toSqlType(parsed_schema)
        java_struct_schema = java_schema_type.dataType()
        msg_schema = StructType.fromJson(json.loads(java_struct_schema.json()))

        udf_deserialize_avro = F.udf(partial(deserialize_avro, schema=fastavro_schema), returnType=msg_schema)

        return udf_deserialize_avro

    def _from_avro(self, column: str, schema: str):
        sc = self._spark.sparkContext
        avro = sc._jvm.org.apache.spark.sql.avro
        f = getattr(getattr(avro, "package$"), "MODULE$").from_avro
        return Column(f(_to_java_column(column), schema))


def _export(
    reader: KafkaReader,
    kafka_options: Dict[str, Any],
    args: Namespace,
) -> DataFrame:
    return reader.read(kafka_options, args.topic)


def _export_avro(
    reader: KafkaAvroReader,
    kafka_options: Dict[str, Any],
    args: Namespace,
) -> DataFrame:
    with args.schema.open("r") as fp:
        avro_schema = fp.read()

    df = reader.read_avro(kafka_options, avro_schema, args.topic)
    if not args.no_unpack:
        df = to_hive_format(df)
    return df


if __name__ == "__main__":
    args = parse_args()

    with args.kafka_options.open("rb") as fp:
        kafka_options = json.load(fp)

    # fetch data
    spark = SparkSession.builder.appName("COCZ-KafkaReader").getOrCreate()
    if args.silent:
        spark.sparkContext.setLogLevel("WARN")

    reader = KafkaAvroReader(spark)

    df = None
    if args.command == Command.EXPORT:
        df = _export(reader, kafka_options, args)
    elif args.command == Command.EXPORT_AVRO:
        df = _export_avro(reader, kafka_options, args)
    else:
        raise NotImplementedError

    if args.limit:
        df = df.limit(args.limit)

    df.write.format(args.format).option("header", True).save(args.output)
