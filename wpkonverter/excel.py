"""Support code for storing data in Excel format"""

# -- Import -------------------------------------------------------------------

from pathlib import Path
from re import sub
from typing import Callable

from pandas import DataFrame, ExcelWriter

from wpkonverter.parsing.csv import RegistrationType

# -- Functions ----------------------------------------------------------------


def modify_header_text(text: str) -> str:
    """Modify a header text

    Args:

        text:

            The text that should be modified

    Returns:

        The modified text

    Examples:

        Modify an example header text

        >>> modify_header_text(
        ...     "Program Points (Companion) 06.10.2026 (Come Together)")
        '06.10.2026 (Come Together)'

    """

    text = sub(r"Program Points (\s*\(Companion\))?\s*", "", text)
    return text


def store_data_workbook(
    data: dict[RegistrationType, DataFrame],
    filepath: Path,
    header_function: Callable[[str], str] | None = None,
) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

        filepath:

            The location of the Excel file that should store the data

        header_function:

            An optional function that is applied to each text in the header
            of the Excel file

    """

    with ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for registration_type, registration_data in data.items():

            sheet_name = repr(registration_type)
            header = list(map(str, registration_data.keys()))

            registration_data.to_excel(
                writer,
                index=False,
                sheet_name=sheet_name,
                header=(
                    list(map(header_function, header))
                    if header_function
                    else header
                ),
            )
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            rows, _ = registration_data.shape

            header_format = workbook.add_format({"bold": True})
            worksheet.set_row(0, cell_format=header_format)

            cell_format = workbook.add_format(
                {"text_wrap": True, "valign": "top"}
            )
            for row in range(1, rows + 1):
                worksheet.set_row(row, cell_format=cell_format)
            writer.sheets[sheet_name].autofit()
