"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from logging import basicConfig, getLogger

from pandas import DataFrame, ExcelWriter

from wpkonverter.cli import get_arguments
from wpkonverter.parsing import parse_csv_file
from wpkonverter.parsing.csv import RegistrationType

# -- Functions ----------------------------------------------------------------


def store_data_workbook(data: dict[RegistrationType, DataFrame]) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

    """

    logger = getLogger(__name__)
    filename = "wpk.xlsx"

    with ExcelWriter(filename, engine="xlsxwriter") as writer:
        for registration_type, registration_data in data.items():

            sheet_name = repr(registration_type)
            registration_data.to_excel(
                writer, index=False, sheet_name=sheet_name
            )
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            rows, columns = registration_data.shape

            header_format = workbook.add_format({"bold": True})
            worksheet.set_row(0, cell_format=header_format)

            logger.debug("Rows: %s, Columns %s", rows, columns)
            cell_format = workbook.add_format(
                {"text_wrap": True, "valign": "top"}
            )
            for row in range(1, rows + 1):
                worksheet.set_row(row, cell_format=cell_format)
            writer.sheets[sheet_name].autofit()

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
