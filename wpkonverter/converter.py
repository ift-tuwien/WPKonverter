"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from pathlib import Path
from logging import basicConfig, getLogger
from sys import exit as sys_exit, stderr

from wpkonverter.cli import get_arguments
from wpkonverter.excel import modify_header_text, store_data_workbook
from wpkonverter.parsing import parse_csv_file
from wpkonverter.parsing.csv import convert_parse_results_data_frame
from wpkonverter.parsing.post_processing import (
    convert_program_points,
    replace_parsed_values,
)

# -- Functions ----------------------------------------------------------------


def exit_error(message: str) -> None:
    """Exit the program with an error status

    Args:

        message:

            The message that should be printed to `stderr` as error reason

    """

    print(message, file=stderr)
    sys_exit(1)


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

    input_filepath = Path(arguments.filepath)

    try:
        registration_types, parsing_results = parse_csv_file(input_filepath)
    except UnicodeDecodeError as error:
        exit_error(f"Unable to read file “{input_filepath}”: {error}")

    converted = replace_parsed_values(convert_program_points(parsing_results))
    parsed_mails = convert_parse_results_data_frame(
        list(zip(registration_types, converted))
    )

    output_filepath = input_filepath.with_suffix(".xlsx")
    store_data_workbook(
        parsed_mails, output_filepath, header_function=modify_header_text
    )
    print(f"Stored data in “{output_filepath}”")
