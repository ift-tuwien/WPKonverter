"""Convert parsed program point data to formats more suitable for a workbook"""

# -- Imports ------------------------------------------------------------------

from logging import getLogger
from typing import Any

from wpkonverter.parsing.grammar.program_point import ProgramPoint

# -- Functions ----------------------------------------------------------------


def get_program_points(
    parsed_mails: list[dict[str, Any]],
) -> tuple[list[str], set[ProgramPoint]]:
    """Determine a set of program points from a list of parsed WPK mails

    Args:

        parsed_mails:

            A list of parsed WPK mails

    Returns:

            - A list of strings containing all keys that store program point
              data and
            - A set containing all the program points contained in the parsed
              data

    Examples:

        Determine set of program points for a single WPK mail

        >>> come_together = ProgramPoint(["06.10.2026", "Come Together"])
        >>> congress_day1 = ProgramPoint(["07.10.2026", "Congress Day 1"])
        >>> parsed_mail = {
        ...     'Program Points': [congress_day1],
        ...     'Program Points (Companion)': [come_together],
        ... }
        >>> parsed_mails = [parsed_mail]
        >>> keys, program_points = get_program_points(parsed_mails)
        >>> keys == ['Program Points', 'Program Points (Companion)']
        True
        >>> program_points == {come_together, congress_day1}
        True

        >>> gala_dinner = ProgramPoint(["07.10.2026", "Gala Dinner"])
        >>> parsed_mails.append({
        ...     'Program Points': [congress_day1],
        ...     'Program Points (Companion)': [come_together,  gala_dinner],
        ... })
        >>> keys, program_points = get_program_points(parsed_mails)
        >>> keys = ['Program Points', 'Program Points (Companion)']
        >>> program_points == {come_together, congress_day1, gala_dinner}
        True

    """

    program_points: set[ProgramPoint] = set()
    program_point_keys: list[str] = []

    for parsed in parsed_mails:
        for key, value in parsed.items():
            if isinstance(value, list) and all(
                (isinstance(element, ProgramPoint) for element in value)
            ):
                # Do not add program point keys multiple times
                if key not in program_point_keys:
                    program_point_keys.append(key)
                program_points |= set(value)

    return program_point_keys, program_points


def convert_program_points(
    parsed_mails: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Add a key for each program point to parsed mail data

    Args:

        parsed_mails:

            A list of parsed WPK mails

    Returns:

        A list of parsed mails where each list of program points is deleted;
        Instead the returned data contains a key for each program point that
        stores if the program point was part of the chosen program points or
        not.

    Examples:

        Convert list of program points for a single WPK mail

        >>> come_together = ProgramPoint(["06.10.2026", "Come Together"])
        >>> congress_day1 = ProgramPoint(["07.10.2026", "Congress Day 1"])
        >>> parsed_mail = {'Program Points': [congress_day1],
        ...                'Program Points (Companion)': [come_together]}
        >>> parsed_mails = convert_program_points([parsed_mail])
        >>> converted_mail = parsed_mails.pop()
        >>> converted_mail # doctest: +NORMALIZE_WHITESPACE
        {'Program Points 06.10.2026 Come Together': False,
         'Program Points 07.10.2026 Congress Day 1': True,
         'Program Points (Companion) 06.10.2026 Come Together': True,
         'Program Points (Companion) 07.10.2026 Congress Day 1': False}

    """

    logger = getLogger(__name__)

    program_point_keys, program_points = get_program_points(parsed_mails)
    program_points_sorted = sorted(program_points)

    logger.debug("Program point keys: %s", program_point_keys)

    converted_mails: list[dict[str, Any]] = []
    for mail in parsed_mails:
        converted: dict[str, Any] = {}
        for key, value in mail.items():
            if key in program_point_keys:
                for program_point in program_points_sorted:
                    chosen = program_point in value
                    converted[f"{key} {program_point}"] = chosen
            else:
                converted[key] = value
        logger.debug(
            "Data with converted program points (%s items): %s",
            len(converted),
            converted,
        )
        converted_mails.append(converted)

    return converted_mails
