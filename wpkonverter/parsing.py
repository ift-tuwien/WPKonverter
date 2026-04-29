"""Parsing support for WPK mail data"""

# -- Imports ------------------------------------------------------------------

from csv import DictReader
from logging import getLogger
from pathlib import Path
from typing import Any

from pandas import DataFrame
from pyparsing import (
    col,
    Combine,
    lineno,
    Literal,
    OneOrMore,
    ParseException,
    ParseResults,
    Regex,
    Suppress,
)

# -- Grammar ------------------------------------------------------------------


def rstrip(tokens):
    """Remove trailing whitespace from input"""

    return tokens[0].rstrip()


def strip(tokens):
    """Remove leading and trailing whitespace from input"""

    return tokens[0].strip()


char = Regex(r"[\s\S]")

from_start = Suppress(Literal("Von:"))
subject_start = Suppress(Literal("Betreff:"))
participant_start = Suppress(Literal("Teilnehmerin/Teilnehmer:"))
organization_start = Suppress(Literal("Unternehmen/ Bildungsinstitut:"))
contact_start = Suppress(Literal("Kontakt:"))
sponsor_start = Suppress(
    Literal("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)
message_start = Suppress(Literal("Nachricht:"))
end = Suppress(Literal("--"))
end_mail = Suppress(
    Literal(
        "This is a notification that a contact form was submitted on your"
        " website (Wiener Produktionstechnik-Kongress"
        " https://wpk.conf.tuwien.ac.at)."
    )
)


# ========
# = From =
# ========

text_from = Combine(OneOrMore(~subject_start + char)).set_parse_action(rstrip)
from_ = from_start + text_from

# ===========
# = Subject =
# ===========

text_subject = Combine(OneOrMore(~participant_start + char)).set_parse_action(
    rstrip
)
subject = subject_start + text_subject("Subject")

# ===============
# = Participant =
# ===============

text_participant = Combine(
    OneOrMore(~organization_start + char)
).set_parse_action(rstrip)
participant = participant_start + text_participant("Participant")

# ================
# = Organization =
# ================

text_organization = Combine(OneOrMore(~contact_start + char)).set_parse_action(
    rstrip
)
organization = organization_start + text_organization("Organization")

# ===========
# = Contact =
# ===========

text_contact = Combine(OneOrMore(~sponsor_start + char)).set_parse_action(
    rstrip
)
contact = contact_start + text_contact("Contact")

# ===========
# = Sponsor =
# ===========

text_sponsor = Combine(OneOrMore(~message_start + char)).set_parse_action(
    rstrip
)
sponsor = sponsor_start + text_sponsor("Sponsor")

# ===========
# = Message =
# ===========

text_message = Combine(
    OneOrMore(~end + char).set_whitespace_chars(" \t")
).set_parse_action(strip)
message = message_start + text_message("Message")

pre_registration = (
    from_
    + subject
    + participant
    + organization
    + contact
    + sponsor
    + message
    + end
    + end_mail
)

# -- Functions ----------------------------------------------------------------


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
