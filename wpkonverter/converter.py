"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from logging import basicConfig, getLogger
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder

from wpkonverter.cli import file_exists
from wpkonverter.parsing import parse_csv_file

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


def store_data_workbook(parsed_mails: list[dict[str, Any]]) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

    """

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Pre-registration"

    assert len(parsed_mails) >= 1, "No registration data provided"

    mail_attributes = parsed_mails[0].keys()
    worksheet.append([attribute.capitalize() for attribute in mail_attributes])

    bold = Font(bold=True)
    start_column = get_column_letter(worksheet.min_column)
    end_column = get_column_letter(worksheet.max_column)
    for row in worksheet[f"{start_column}1:{end_column}1"]:
        for cell in row:
            cell.font = bold

    dimension_holder = DimensionHolder(worksheet=worksheet)

    for column in range(worksheet.min_column, worksheet.max_column + 1):
        dimension_holder[get_column_letter(column)] = ColumnDimension(
            worksheet, min=column, max=column, width=40
        )

    worksheet.column_dimensions = dimension_holder

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

    arguments = get_arguments()

    basicConfig(
        encoding="utf-8",
        format="{asctime} {levelname:7} {message}",
        level=arguments.log.upper(),
        style="{",
    )

    logger = getLogger(__name__)
    logger.info("CLI Arguments: %s", arguments)

    try:
        parsed_mails = parse_csv_file(arguments.filepath)
        store_data_workbook(parsed_mails)
    except UnicodeDecodeError as error:
        print(f"Unable to read file “{arguments.filepath}”: {error}")
