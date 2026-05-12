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
from pyparsing import ParserElement, ParseException

from wpkonverter.parsing.error import generate_error_message
from wpkonverter.parsing.program_point import convert_program_points
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
    parsing_results: list[tuple[RegistrationType, dict[str, Any]]],
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
        logger.debug("Registration data: %s", registration)
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

    Examples:

        Get type for student registration

        >>> subject = ("Wiener Produktionstechnik-Kongress „Studierende "
        ...            "Anmeldung WPK2026“")
        >>> get_registration_type(subject)
        Student

        Get type for participant registration

        >>> subject = ("Wiener Produktionstechnik-Kongress „TeilnehmerIn "
        ...            "Anmeldung WPK2026“")
        >>> get_registration_type(subject)
        Participant

    """

    pattern_to_type = (
        (re_pattern("Vorregistrierung"), RegistrationType.PRE_REGISTRATION),
        (
            re_pattern(r"Participant|Teilnehmer"),
            RegistrationType.PARTICIPANT,
        ),
        (
            re_pattern(r"Speaker (Anmeldung|Registration)"),
            RegistrationType.SPEAKER,
        ),
        (re_pattern("Sponsoren Anmeldung"), RegistrationType.SPONSOR),
        (re_pattern("Student|Studierende"), RegistrationType.STUDENT),
    )

    for pattern, registration_type in pattern_to_type:
        if pattern.search(subject):
            return registration_type

    return RegistrationType.UNKOWN


def get_grammar(registration_type: RegistrationType) -> ParserElement | None:
    """Get the grammar definition for a certain registration type


    Args:

        registration_type:

            The type of the registration data

    Returns:

        The grammar definition for the registration type or ``None`` if no
        grammar for the registration type is known

    """

    type_to_grammar = {
        RegistrationType.PRE_REGISTRATION: pre_registration,
        RegistrationType.SPEAKER: speaker_registration,
    }

    return type_to_grammar.get(registration_type)


def parse_csv_file(filepath: Path) -> dict[RegistrationType, DataFrame]:
    """Parse CSV mails for registration data

    Args:

        filepath:

            Path to CSV file that contains registration mails

    Returns:

        A list of parsed mail data

    """

    logger = getLogger(__name__)

    registration_types: list[RegistrationType] = []
    parsing_results: list[dict[str, Any]] = []
    with open(filepath, newline="", encoding="utf-8-sig") as csvfile:
        reader = DictReader(csvfile)

        for mail_number, row in enumerate(reader, start=1):
            registration_type = get_registration_type(row["Betreff"])
            grammar = get_grammar(registration_type)
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
                registration_types.append(registration_type)
                parsing_results.append(parsed.as_dict())
            except ParseException as error:
                print(
                    f"Unable to parse data in mail {mail_number}:\n\n"
                    f"{generate_error_message(text, error)}\n",
                    file=stderr,
                )
                continue

    converted = convert_program_points(parsing_results)
    registration_data = list(zip(registration_types, converted))

    return convert_parse_results_data_frame(registration_data)
