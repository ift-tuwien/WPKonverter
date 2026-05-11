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

from wpkonverter.parsing.error import generate_error_message
from wpkonverter.parsing.grammar.pre_registration import pre_registration
from wpkonverter.parsing.grammar.speaker import speaker_registration

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

    def __repr__(self):
        """Get a textual representation of the registration type

        Returns:

            A text representing the registration type

        Examples:

            Get string representation of pre-registration type

            >>> RegistrationType.PRE_REGISTRATION
            Pre-Registration

        """

        name = self.name
        name = "-".join(part.capitalize() for part in name.split("_"))

        return name


# -- Functions ----------------------------------------------------------------


def convert_parse_results_data_frame(
    parsing_results: list[tuple[RegistrationType, ParseResults]],
) -> dict[RegistrationType, DataFrame]:
    """Convert parsing data into data frame

    Args:

        parsing_results:

            A list of tuples containing the registration type and the parsing
            result of the mail

    Returns:

        A dictionary that stores the registration data for each registration
        type as data frame

    """

    logger = getLogger(__name__)
    registration_data: dict[RegistrationType, dict[str, Any]] = {}

    for registration_type, registration in parsing_results:
        logger.debug("Registration type: %s", registration_type)
        logger.debug("Registration data: %s", registration.as_dict())
        if registration_data.get(registration_type) is None:
            registration_data[registration_type] = {}
        registration_dict = registration_data[registration_type]

        for attribute, result in registration.items():
            if registration_dict.get(attribute) is None:
                registration_dict[attribute] = []
            values = registration_dict.get(attribute)
            assert isinstance(values, list)
            values.append(result)

    logger.debug("Converted parsing data: %s", registration_data)

    frames: dict[RegistrationType, DataFrame] = {}
    for registration_type, registration_dict in registration_data.items():
        frames[registration_type] = DataFrame(data=registration_dict)

    return frames


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
        (
            re_pattern(r"(Participant|TeilnehmerIn) registration"),
            RegistrationType.PARTICIPANT,
        ),
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


def parse_csv_file(filepath: Path) -> dict[RegistrationType, DataFrame]:
    """Parse CSV mails for registration data

    Args:

        filepath:

            Path to CSV file that contains registration mails

    Returns:

        A list of parsed mail data

    """

    logger = getLogger(__name__)
    type_to_grammar = {
        RegistrationType.PRE_REGISTRATION: pre_registration,
        RegistrationType.SPEAKER: speaker_registration,
    }

    parsing_results: list[tuple[RegistrationType, ParseResults]] = []
    with open(filepath, newline="", encoding="utf-8-sig") as csvfile:
        reader = DictReader(csvfile)

        for mail_number, row in enumerate(reader, start=1):
            logger.debug("Row: %s", row)
            registration_type = get_registration_type(row["Betreff"])
            logger.debug("Registration type: %s", registration_type)
            grammar = type_to_grammar.get(registration_type)
            if grammar is None:
                print(
                    f"No grammar for registration type “{registration_type}” "
                    f"of mail {mail_number}",
                    file=stderr,
                )
                continue

            text = row["Text"]
            logger.debug("Mail text: %s", text)
            try:
                parsed = grammar.parse_string(text, parse_all=True)
                parsing_results.append((registration_type, parsed))
            except ParseException as error:
                print(
                    f"Unable to parse data in mail {mail_number}:\n\n"
                    f"{generate_error_message(text, error)}\n",
                    file=stderr,
                )
                continue

    return convert_parse_results_data_frame(parsing_results)
