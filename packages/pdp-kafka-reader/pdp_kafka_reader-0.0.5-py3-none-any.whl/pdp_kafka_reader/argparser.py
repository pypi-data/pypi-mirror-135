import argparse
import enum
from pathlib import Path


class Command(enum.Enum):
    EXPORT = "export"
    EXPORT_AVRO = "export-avro"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="kafka-reader",
        description="Read and export messages from Kafka",
    )
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    parser_common = argparse.ArgumentParser(add_help=False)
    parser_common.add_argument(
        "-k",
        "--kafka-options",
        type=Path,
        required=True,
        help="Config file with Kafka options in JSON format",
    )
    parser_common.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output file path",
    )
    parser_common.add_argument(
        "-f",
        "--format",
        choices=["csv", "parquet"],
        required=False,
        default="parquet",
        help="Output format",
    )
    parser_common.add_argument(
        "-t",
        "--topic",
        type=str,
        required=False,
        default=None,
        help="Kafka topic to read data from",
    )
    parser_common.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=None,
        help="Maximum number of messages collected to driver",
    )
    parser_common.add_argument(
        "--silent",
        action="store_true",
        default=False,
        help="Do not print spark INFO logs",
    )

    # create the parser for the "export" command
    parser_export = subparsers.add_parser(
        "export",
        parents=[parser_common],
        help="Export messages",
    )
    parser_export.set_defaults(command=Command.EXPORT)

    # create the parser for the "export-avro" command
    parser_export_avro = subparsers.add_parser(
        "export-avro",
        parents=[parser_common],
        help="Deserialize and export Avro messages",
    )
    parser_export_avro.set_defaults(command=Command.EXPORT_AVRO)
    parser_export_avro.add_argument(
        "-s",
        "--schema",
        type=Path,
        required=True,
        help="Avro schema in JSON format",
    )
    parser_export_avro.add_argument(
        "--no-unpack",
        action="store_true",
        default=False,
        help="Do not unpack Avro structures into flat columns",
    )

    return parser.parse_args()
