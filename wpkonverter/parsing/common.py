"""Common parsing functionality"""

# -- Imports ------------------------------------------------------------------

from enum import auto, Enum
from logging import getLogger
from typing import Any

from pandas import DataFrame
from pyparsing import (
    col,
    Keyword,
    lineno,
    Optional,
    ParseException,
    ParseResults,
    SkipTo,
    Suppress,
)

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


def rstrip(tokens):
    """Remove trailing whitespace from input"""

    return tokens[0].rstrip()


def strip(tokens):
    """Remove leading and trailing whitespace from input"""

    return tokens[0].strip()


def generate_error_message(text: str, error: ParseException) -> str:
    """Generate a human readable parsing error message

    Args:

        text:

            The parsed text that produced an error

        error:

            The error that occurred while parsing ``text``

    Returns:

        An error message that shows the user where the parsing error occurred

    """

    line_number = lineno(error.loc, text)
    column_number = col(error.loc, text)
    lines = text.splitlines()
    quote_symbol = "> "
    error_indent = " " * (len(quote_symbol) + column_number)

    error_message: list[str] = []
    for line in lines[line_number - 5 : line_number]:
        error_message.append(f"{quote_symbol}{line}")
    error_message.append(f"{error_indent}^")
    error_message.append(f"{error_indent}{error}")
    for line in lines[line_number : line_number + 1]:
        error_message.append(f"{quote_symbol}{line}")

    return "\n".join(error_message)


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

    logger.debug("Parsing results: %s", parsing_results)

    for registration_type, registration in parsing_results:
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


# -- Grammar ------------------------------------------------------------------

from_start = Suppress(Keyword("Von:") ^ Keyword("From:"))
subject_start = Suppress(Keyword("Betreff:") ^ Keyword("Subject:"))

participant_start = Suppress(
    Keyword("Teilnehmerin/Teilnehmer:") ^ Keyword("Participant:")
)
speaker_start = Suppress(
    Optional(Keyword("Speakerinnen/")) + Keyword("Speaker:")
)
sponsor_start = Suppress(Keyword("Sponsoren:"))
attendee_start = participant_start ^ speaker_start ^ sponsor_start

# ========
# = From =
# ========

text_from = SkipTo(subject_start).set_parse_action(rstrip)
from_ = from_start + text_from

# ===========
# = Subject =
# ===========

text_subject = SkipTo(attendee_start).set_parse_action(rstrip)
subject = subject_start + text_subject("Subject")

from_and_subject = from_ + subject
