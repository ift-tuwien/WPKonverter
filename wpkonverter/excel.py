"""Support code for storing data in Excel format"""

# -- Import -------------------------------------------------------------------

from pathlib import Path
from re import sub
from typing import Callable

from pandas import DataFrame, ExcelWriter
from xlsxwriter import Workbook
from xlsxwriter.format import Format

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


def get_header_format(
    workbook: Workbook, registration_type: RegistrationType
) -> Format:
    """Get the header format for a specific registration type

    Args:

        workbook:

            The workbook where the header format should be added

        registration_type:

            The registration type for which we want to determine the header
            format

    Returns:

        The cell format for the header of the given registration type

    """

    base_format = {"bold": True, "bottom": True}
    registration_type_to_header_format = {
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

    header_format = registration_type_to_header_format[registration_type]
    return workbook.add_format(header_format)


# pylint: disable=too-many-locals


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
            header_text = map(str, registration_data.keys())
            header = list(
                map(header_function, header_text)
                if header_function
                else header_text
            )

            registration_data.to_excel(
                writer,
                index=False,
                sheet_name=sheet_name,
                startrow=1,
                header=False,
            )
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            rows, _ = registration_data.shape

            header_format = get_header_format(workbook, registration_type)
            for column, value in enumerate(header):
                worksheet.write(0, column, value, header_format)

            cell_format = workbook.add_format({
                "text_wrap": True,
                "valign": "top",
            })
            for row in range(1, rows + 1):
                worksheet.set_row(row, cell_format=cell_format)
            writer.sheets[sheet_name].autofit()


# pylint: enable=too-many-locals
