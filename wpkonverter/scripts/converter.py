"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from csv import DictReader

from openpyxl import Workbook
from pyparsing import ParseException, ParseResults

from wpkonverter.cli import file_exists
from wpkonverter.parsing import mail, mail_attributes

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


def store_data_workbook(parsed_mails: list[ParseResults]) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

    """

    workbook = Workbook()
    worksheet = workbook.active

    worksheet.append([attribute.capitalize() for attribute in mail_attributes])

    for parsed_mail in parsed_mails:
        worksheet.append(
            [parsed_mail[attribute] for attribute in mail_attributes]
        )

    filename = "wpk.xlsx"
    workbook.save(filename)
    print(f"Stored data in “{filename}”")


# -- Main ---------------------------------------------------------------------


def main() -> None:
    """Convert WPK mail registration data"""

    filepath = get_arguments().filepath

    with open(filepath, newline="", encoding="utf8") as csvfile:
        reader = DictReader(csvfile)
        parsed_mails: list[ParseResults] = []
        for row in reader:
            text = row["Text"]
            print(text)
            print("—" * 50)
            try:
                parsed_mail = mail.parse_string(text)
                parsed_mails.append(parsed_mail)

                print("Parsed Data:\n")
                for attribute in mail_attributes:
                    print(f"{attribute}: {parsed_mail[attribute]}")
                    print("—")
            except ParseException:
                print("Unable to parse data\n")

        store_data_workbook(parsed_mails)
