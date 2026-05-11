"""Support code for storing data in Excel format"""

# -- Import -------------------------------------------------------------------

from logging import getLogger

from pandas import DataFrame, ExcelWriter

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
