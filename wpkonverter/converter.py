"""Convert WPK mail registration data"""

# -- Import -------------------------------------------------------------------

from logging import basicConfig, getLogger

from wpkonverter.cli import get_arguments
from wpkonverter.excel import store_data_workbook
from wpkonverter.parsing import parse_csv_file

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
