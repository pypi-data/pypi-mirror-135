from pathlib import Path

from importlib_resources import files

_PACKAGE_PATH = files("pdp_kafka_reader")
SPARK_AVRO_JAR_PATH: Path = _PACKAGE_PATH.joinpath(
    "jars/spark-avro_2.11-2.4.0.cloudera2.jar"
)
