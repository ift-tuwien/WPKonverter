"""Parse CSV data"""

# -- Imports ------------------------------------------------------------------

from csv import DictReader
from logging import getLogger
from pathlib import Path
from typing import Any

from pandas import DataFrame
from pyparsing import (
    ParseException,
    ParseResults,
)

from wpkonverter.parsing.pre_registration import pre_registration
from wpkonverter.parsing.common import generate_error_message

# -- Functions ----------------------------------------------------------------


def parse_csv_file(filepath: Path) -> DataFrame:
    """Parse CSV mails for registration data

    Args:

        filepath:

            Path to CSV file that contains registration mails

    Returns:

        A list of parsed mail data

    """

    logger = getLogger(__name__)

    parsing_results: list[ParseResults] = []
    with open(filepath, newline="", encoding="utf8") as csvfile:
        reader = DictReader(csvfile)

        for mail_number, row in enumerate(reader, start=1):
            text = row["Text"]
            logger.debug("Mail text: %s", text)
            try:
                parsing_results.append(
                    pre_registration.parse_string(text, parse_all=True)
                )
            except ParseException as error:
                print(
                    f"Unable to parse data in mail {mail_number}:\n\n"
                    f"{generate_error_message(text, error)}\n"
                )
                continue
        registration_data: dict[str, Any] = {}
        if len(parsing_results) >= 1:
            for attribute in parsing_results[0].keys():
                registration_data[attribute] = []
            for parse_result in parsing_results:
                for attribute, result in parse_result.items():
                    registration_data[attribute].append(result)

    logger.debug("Registration Data: %s", registration_data)
    return DataFrame(data=registration_data)
