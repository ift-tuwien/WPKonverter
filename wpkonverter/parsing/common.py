"""Common parsing functionality"""

# -- Imports ------------------------------------------------------------------

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
