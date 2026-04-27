"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from argparse import ArgumentParser, Namespace
from logging import basicConfig, getLogger

from pandas import DataFrame
from styleframe import StyleFrame, Styler

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


def store_data_workbook(data: DataFrame) -> None:
    """Store registration data in Excel file

    Args:

        data:

            The registration data that should be stored in the Excel file

    """

    default_style = Styler(font_size=12)
    style_frame = StyleFrame(data, styler_obj=default_style)
    header_style = Styler(bold=True, font_size=16)
    style_frame.apply_headers_style(styler_obj=header_style)
    style_frame.set_column_width(columns=style_frame.columns, width=40)

    filename = "wpk.xlsx"
    writer = style_frame.to_excel(filename)
    writer.close()

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
