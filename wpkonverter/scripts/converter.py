# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from csv import DictReader

from wpkonverter.cli import file_exists

# -- Functions ----------------------------------------------------------------


def get_arguments() -> Namespace:
    """Parse command line arguments

    Returns:

        An object that contains the given command line arguments

    """

    parser = ArgumentParser(
        description="Extract data from WPK registration mails"
    )
    parser.add_argument(
        "filepath",
        type=file_exists,
        help="WPK mail information in CSV format",
    )

    return parser.parse_args()


# -- Main ---------------------------------------------------------------------


def main():
    """Convert WPK mail registration data"""

    filepath = get_arguments().filepath

    with open(filepath, newline="", encoding="utf8") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            print(row["Text"])
            print("—" * 50)
