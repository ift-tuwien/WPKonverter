"""Utility code for working with command line data"""

# -- Imports ------------------------------------------------------------------

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path

# -- Functions ----------------------------------------------------------------


def file_exists(filepath: str) -> str:
    """Check if the given path points to an existing file

    Args:

        filepath:

                Path to the file

    Raises:

        An argument type error in case the the filepath does not point to an
        existing file

    Returns:


        The given filepath on success

    """

    if not Path(filepath).exists():
        raise ArgumentTypeError(f"“{filepath}” does not exist")

    if not Path(filepath).is_file():
        raise ArgumentTypeError(f"“{filepath}” does not point to a file")

    return filepath


def get_arguments() -> Namespace:
    """Parse command line arguments

    Returns:

        An object that contains the given command line arguments

    """

    parser = ArgumentParser(
        description="Extract data from WPK registration mails"
    )

    parser.add_argument(
        "--log",
        choices=("debug", "info", "warning", "error", "critical"),
        default="warning",
        required=False,
        help="minimum log level",
    )

    parser.add_argument(
        "filepath",
        type=file_exists,
        help="WPK mail information in CSV format",
    )

    return parser.parse_args()
