"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from csv import DictReader
from re import split
from typing import NamedTuple

from wpkonverter.cli import file_exists

# -- Types --------------------------------------------------------------------

type Remainder = str
type Parsed[T] = tuple[T, Remainder]

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


def parse_name(text: str) -> Parsed[str]:
    """Parse participation name

    Args:

        text:

            The input that should be parsed

    Returns:

        A tuple containing the name and the remainder of the input text

    """

    _, remainder = split(r"Teilnehmerin/Teilnehmer:\s*", text, maxsplit=1)
    name, remainder = split(r"\r?\n", remainder, maxsplit=1)
    return name, remainder


# -- Classes ------------------------------------------------------------------


class RegistrationData(NamedTuple):
    """Store parsed registration data"""

    name: str


# -- Main ---------------------------------------------------------------------


def main():
    """Convert WPK mail registration data"""

    filepath = get_arguments().filepath

    with open(filepath, newline="", encoding="utf8") as csvfile:
        reader = DictReader(csvfile)
        parsed_data = []
        for row in reader:
            text = row["Text"]
            print(text)
            print("—" * 50)
            name, _ = parse_name(text)
            parsed_data.append(RegistrationData(name=name))

    print("Parsed Data:\n")
    for record in parsed_data:
        print(record)
