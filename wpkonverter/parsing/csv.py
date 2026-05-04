"""Parse CSV data"""

# -- Imports ------------------------------------------------------------------

from csv import DictReader
from enum import auto, Enum
from logging import getLogger
from pathlib import Path
from re import compile as re_pattern
from sys import stderr
from typing import Any

from pandas import DataFrame
from pyparsing import (
    ParseException,
    ParseResults,
)

from wpkonverter.parsing.pre_registration import pre_registration
from wpkonverter.parsing.common import generate_error_message

# -- Classes ------------------------------------------------------------------


class RegistrationType(Enum):
    """Possible registration types"""

    PRE_REGISTRATION = auto()
    """Pre-Registration"""

    PARTICIPANT = auto()
    """General Participant"""

    SPEAKER = auto()
    """Speaker"""

    SPONSOR = auto()
    """Sponsor"""

    STUDENT = auto()
    """Student"""

    UNKOWN = auto()
    "Unknown registration type"


# -- Functions ----------------------------------------------------------------


def get_registration_type(subject: str) -> RegistrationType:
    """Determine participation type from mail subject

    Args:

        subject:

            The subject line from the registration mail

    Returns:

        The type of the mail registration

    """

    pattern_to_type = (
        (re_pattern("Vorregistrierung"), RegistrationType.PRE_REGISTRATION),
        (re_pattern("Participant registration"), RegistrationType.PARTICIPANT),
        (
            re_pattern(r"Speaker (Anmeldung|Registration)"),
            RegistrationType.SPEAKER,
        ),
        (re_pattern("Sponsoren Anmeldung"), RegistrationType.SPONSOR),
        (re_pattern("Student registration"), RegistrationType.STUDENT),
    )

    for pattern, registration_type in pattern_to_type:
        if pattern.search(subject):
            return registration_type

    return RegistrationType.UNKOWN


def convert_parse_results_data_frame(parsing_results: list[ParseResults]):
    """Convert parsing data into data frame

    Args:

        parsing_results:

            A list of parsing results

    Returns:

        A data frame that stores the parsed data

    """

    registration_data: dict[str, Any] = {}
    if len(parsing_results) >= 1:
        for attribute in parsing_results[0].keys():
            registration_data[attribute] = []
        for parse_result in parsing_results:
            for attribute, result in parse_result.items():
                registration_data[attribute].append(result)

    getLogger(__name__).debug("Converted parsing data: %s", registration_data)
    return DataFrame(data=registration_data)


def parse_csv_file(filepath: Path) -> DataFrame:
    """Parse CSV mails for registration data

    Args:

        filepath:

            Path to CSV file that contains registration mails

    Returns:

        A list of parsed mail data

    """

    logger = getLogger(__name__)

    pre_registration_parsing_results: list[ParseResults] = []
    with open(filepath, newline="", encoding="utf-8-sig") as csvfile:
        reader = DictReader(csvfile)

        for mail_number, row in enumerate(reader, start=1):
            logger.debug("Row: %s", row)
            registration_type = get_registration_type(row["Betreff"])
            logger.debug("Registration type: %s", registration_type)
            text = row["Text"]
            logger.debug("Mail text: %s", text)
            try:
                match registration_type:
                    case RegistrationType.PRE_REGISTRATION:
                        parser_results = pre_registration.parse_string(
                            text, parse_all=True
                        )
                        pre_registration_parsing_results.append(parser_results)
            except ParseException as error:
                print(
                    f"Unable to parse data in mail {mail_number}:\n\n"
                    f"{generate_error_message(text, error)}\n",
                    file=stderr,
                )
                continue

    return convert_parse_results_data_frame(pre_registration_parsing_results)
