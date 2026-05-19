"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from pathlib import Path
from logging import basicConfig, getLogger
from sys import exit as sys_exit, stderr

from chardet import UniversalDetector

from wpkonverter.cli import get_arguments
from wpkonverter.excel import modify_header_text, store_data_workbook
from wpkonverter.parsing import parse_csv_file
from wpkonverter.parsing.csv import convert_parse_results_data_frame
from wpkonverter.parsing.post_processing import convert_program_points

# -- Functions ----------------------------------------------------------------


def exit_error(message: str) -> None:
    """Exit the program with an error status

    Args:

        message:

            The message that should be printed to `stderr` as error reason

    """

    print(message, file=stderr)
    sys_exit(1)


def determine_encoding(filepath: Path) -> str | None:
    """Determine the encoding of the given file

    Args:

        filepath:

            The path to the file for which the encoding should be determined

    Returns:

        The encoding of the given file

    """

    detector = UniversalDetector()
    with open(filepath, "rb") as filedescriptor:
        for line in filedescriptor:
            detector.feed(line)
            if detector.done:
                break
    result = detector.close()
    return result["encoding"]


# -- Main ---------------------------------------------------------------------


def main() -> None:
    """Convert WPK mail registration data"""

    arguments = get_arguments()

    basicConfig(
        format="{asctime} {levelname:7} {message}",
        level=arguments.log.upper(),
        style="{",
    )

    logger = getLogger(__name__)
    logger.info("CLI Arguments: %s", arguments)

    input_filepath = Path(arguments.filepath)

    encoding = determine_encoding(input_filepath)
    if encoding is None:
        exit_error(
            f"Unable to determine text encoding of file “{input_filepath}”"
        )

    registration_types, parsing_results = parse_csv_file(input_filepath)

    converted = convert_program_points(parsing_results)
    parsed_mails = convert_parse_results_data_frame(
        list(zip(registration_types, converted))
    )

    output_filepath = input_filepath.with_suffix(".xlsx")
    store_data_workbook(
        parsed_mails, output_filepath, header_function=modify_header_text
    )
    print(f"Stored data in “{output_filepath}”")
