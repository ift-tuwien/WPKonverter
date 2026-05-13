"""Support code for storing data in Excel format"""

# -- Import -------------------------------------------------------------------

from pathlib import Path
from re import sub
from typing import Any, Callable

from pandas import DataFrame, ExcelWriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

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


def get_header_format(registration_type: RegistrationType) -> dict[str, Any]:
    """Get the header format for a specific registration type

    Args:

        registration_type:

            The registration type for which we want to determine the header
            format

    Returns:

        The cell format for the header of the given registration type

    """

    base_format: dict[str, Any] = {"bold": True, "bottom": True}
    registration_type_to_header_format: dict[
        RegistrationType, dict[str, Any]
    ] = {
        RegistrationType.PRE_REGISTRATION: (
            base_format
            | {
                "fg_color": "#C6E8E9",
            }
        ),
        RegistrationType.PARTICIPANT: base_format,
        RegistrationType.SPEAKER: (
            base_format
            | {
                "fg_color": "#E4C5FB",
            }
        ),
        RegistrationType.SPONSOR: base_format,
        RegistrationType.STUDENT: base_format,
        RegistrationType.UNKOWN: base_format,
    }

    return registration_type_to_header_format[registration_type]


def get_cell_format() -> dict[str, Any]:
    """Get the formatting options for a Excel cell

    Returns:

        The formatting options for a non-header Excel cell

    """

    return {
        "text_wrap": True,
        "valign": "top",
    }


def get_bool_cell_format() -> dict[str, Any]:
    """Get the formatting options for an boolean Excel cell

    Returns:

        The formatting options for a non-header boolean Excel cell

    """

    return get_cell_format() | {"checkbox": True}


def write_header(
    workbook: Workbook,
    worksheet: Worksheet,
    header: list[str],
    cell_format: dict[str, Any],
) -> None:
    """Add header data to a worksheet

    Args:

        workbook:

            The workbook that contains ``worksheet``

        worksheet:

            The worksheet that should store the header data

        header:

            The header that should be added to ``worksheet``

        formatting:

            The cell format for the header

    """

    header_format = workbook.add_format(cell_format)
    for column, value in enumerate(header):
        worksheet.write(0, column, value, header_format)


def write_cells(workbook, worksheet, registration_data):
    """fill"""
    cell_format = workbook.add_format(get_cell_format())
    bool_format = workbook.add_format(get_bool_cell_format())

    for row_number, row in enumerate(
        registration_data.itertuples(index=False), start=1
    ):
        for column_number, value in enumerate(row):

            value_format = (
                bool_format if isinstance(value, bool) else cell_format
            )

            worksheet.write(
                row_number,
                column_number,
                value,
                value_format,
            )


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

            workbook = writer.book
            worksheet = workbook.add_worksheet(repr(registration_type))

            header_text = map(str, registration_data.keys())
            header = list(
                map(header_function, header_text)
                if header_function
                else header_text
            )
            write_header(
                workbook,
                worksheet,
                header,
                cell_format=get_header_format(registration_type),
            )
            write_cells(workbook, worksheet, registration_data)

            worksheet.autofit()
