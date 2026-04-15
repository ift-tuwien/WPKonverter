"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from csv import DictReader
from re import split

from openpyxl import Workbook

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


def parse_organization(text: str) -> Parsed[str]:
    """Parse organization/university

    Args:

        text:

            The input that should be parsed

    Returns:

        A tuple containing the organization name and the remainder of the
        input text

    """

    _, remainder = split(
        r"Unternehmen/\s*Bildungsinstitut:\s*", text, maxsplit=1
    )
    organization, remainder = split(r"\r?\n", remainder, maxsplit=1)

    return organization, remainder


def store_data_workbook(data: list[RegistrationData]) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

    """

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(RegistrationData.attribute_names())

    for record in data:
        worksheet.append(record.values())

    filename = "wpk.xlsx"
    workbook.save(filename)
    print(f"Stored data in “{filename}”")


# -- Classes ------------------------------------------------------------------


class RegistrationData:
    """Store parsed registration data"""

    attributes = {
        "name": "Participant",
        "organization": "Organization",
    }

    def __init__(self, name: str, organization: str):
        self.name = name
        self.organization = organization

    @classmethod
    def attribute_names(cls) -> list[str]:
        """Get a string representation of the attributes

        Returns:

            A list of human readable name for the stored attributes

        """

        return list(cls.attributes.values())

    def values(self) -> list:
        """Get a list of all registration values

        Returns:

            All values of the registration data

        """

        cls = type(self)

        return [getattr(self, attribute) for attribute in cls.attributes]

    def __repr__(self) -> str:
        """Get the string representation of the registration data

        Returns:

            A text containing the registration attributes and their values

        """

        cls = type(self)

        return ", ".join([
            f"{attribute}: {getattr(self, attribute)}"
            for attribute in cls.attributes
        ])


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
            name, remainder = parse_name(text)
            organization, remainder = parse_organization(remainder)
            parsed_data.append(
                RegistrationData(name=name, organization=organization)
            )

    print("Parsed Data:\n")
    for record in parsed_data:
        print(record)

    store_data_workbook(parsed_data)
