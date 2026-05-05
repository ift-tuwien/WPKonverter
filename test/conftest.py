"""Configuration for pytest"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path
from typing import Any

from pyparsing import ParserElement
from pytest import fixture

# -- Classes ------------------------------------------------------------------


# pylint: disable=too-few-public-methods


class Checkers:
    """Share testing functions between modules"""

    @staticmethod
    def check_grammar(
        grammar: ParserElement, filepath: Path, expected: dict[str, Any]
    ) -> None:
        """Check if parsing a file results in the expected result

        Args:

            grammar:

                The grammar that should be used to parse the file

            filepath:

                The path of the file that should be parsed

            expected:

                The expected result of the parsing process

        """

        with open(filepath, encoding="utf-8") as file_content:
            text = file_content.read()

        parsed = grammar.parse_string(text, parse_all=True)
        assert parsed.as_dict() == expected


# pylint: enable=too-few-public-methods

# -- Fixtures -----------------------------------------------------------------


@fixture
def checkers():
    """Checking functionality"""

    return Checkers
