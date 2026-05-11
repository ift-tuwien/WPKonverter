"""Test program point parsing"""

# -- Imports ------------------------------------------------------------------

from datetime import datetime

from wpkonverter.parsing.grammar.program_point import (
    date,
    program_point,
    program_points,
    ProgramPoint,
)

# -- Tests --------------------------------------------------------------------


def test_date():
    """Test parsing of a date"""

    text = "6.10.2026"
    parsed = date.parse_string(text, parse_all=True)
    parsed_list = parsed.as_list()
    assert len(parsed_list) == 1
    assert isinstance(parsed_list[0], datetime)
    assert parsed_list[0] == datetime.strptime(text, "%d.%m.%Y")


def test_program_point():
    """Test parsing of single program point"""

    text = "Dienstag 6.10.2026 - Come Together"
    parsed = program_point.parse_string(text, parse_all=True)
    parsed_list = parsed.as_list()
    assert len(parsed_list) == 1
    assert isinstance(parsed_list[0], ProgramPoint)
    assert parsed_list[0] == ProgramPoint(["6.10.2026", "Come Together"])


def test_program_points():
    """Test parsing of multiple program points"""

    text = """
    Dienstag 6.10.2026 - Come Together,
    Mittwoch 7.10.2026 - 1. Kongresstag,
    Mittwoch 7.10.2026 - Galadinner,
    Donnerstag 8.10.2026 - 2. Kongresstag
    """

    parsed = program_points.parse_string(text, parse_all=True)
    assert parsed.as_list() == [
        "• 06.10.2026 (Come Together)\n"
        "• 07.10.2026 (Congress Day 1)\n"
        "• 07.10.2026 (Gala Dinner)\n"
        "• 08.10.2026 (Congress Day 2)"
    ]

    text = "Wednesday 7.10.2026 - Congress Day 1"
    parsed = program_points.parse_string(text, parse_all=True)
    assert parsed.as_list() == ["• 07.10.2026 (Congress Day 1)"]

    text = "Tuesday 6.10.2026 - Come Together"
    parsed = program_points.parse_string(text, parse_all=True)
    assert parsed.as_list() == ["• 06.10.2026 (Come Together)"]
