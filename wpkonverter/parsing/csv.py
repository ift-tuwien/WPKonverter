"""Parse CSV data"""

# -- Imports ------------------------------------------------------------------

from csv import DictReader
from logging import getLogger
from pathlib import Path
from re import compile as re_pattern
from sys import stderr

from pandas import DataFrame
from pyparsing import (
    ParseException,
    ParseResults,
)

from wpkonverter.parsing.common import (
    convert_parse_results_data_frame,
    generate_error_message,
    RegistrationType,
)
from wpkonverter.parsing.grammar.pre_registration import pre_registration
from wpkonverter.parsing.grammar.speaker import speaker_registration

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
