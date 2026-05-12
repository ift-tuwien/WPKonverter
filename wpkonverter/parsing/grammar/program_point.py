"""Parse program point information"""

# -- Imports ------------------------------------------------------------------

from datetime import datetime
from re import sub
from typing import Any

from pyparsing import (
    CharsNotIn,
    Combine,
    DelimitedList,
    Keyword,
    nums,
    Optional,
    Suppress,
    Word,
)

from wpkonverter.parsing.grammar.common import strip

# -- Classes ------------------------------------------------------------------


class ProgramPoint:
    """Store data about a single WPK program point"""

    def __init__(self, tokens):
        """Initialize the program point with the given tokens

        Args:

            tokens:

                The parsing tokens used to construct the program point

        """

        self.date = (
            tokens[0]
            if isinstance(tokens[0], datetime)
            else datetime.strptime(tokens[0], "%d.%m.%Y")
        )
        self.description = tokens[1]

        self._unify_description()

    def __eq__(self, other):
        """Check if two program points are equal

        Args:

            other:

                The other object that should be compared to this program point

        Return:

            ``True`` if ``self`` and ``other`` are equal, ``False`` otherwise

        Examples:

            >>> date = "4.5.2006"

            The same program points are equal

            >>> (ProgramPoint([date, "Dinner"]) ==
            ...  ProgramPoint([date, "Dinner"]))
            True

            Different program points are not equal

            >>> (ProgramPoint([date, "Dinner"]) ==
            ...  ProgramPoint([date, "Supper"]))
            False

        """

        if isinstance(other, ProgramPoint):
            return (
                self.date == other.date
                and self.description == other.description
            )

        return NotImplemented

    def __hash__(self) -> int:
        """Get hash value of program point

        Returns:

            The hash value of the program point

        Examples:

            Check if two sets containing the same program points are equal

            >>> ({ProgramPoint(["1.1.1970", "Something"]),
            ...   ProgramPoint(["1.1.1970", "Something"]),
            ...   ProgramPoint(["2.1.1970", "Something"])} ==
            ...  {ProgramPoint(["2.1.1970", "Something"]),
            ...   ProgramPoint(["1.1.1970", "Something"])})
            True

        """

        return hash((self.date, self.description))

    def __lt__(self, other: Any):
        """Check if a program point is smaller than another object

        Args:

            other:

                The other object that should be compared to this program point

        Return:

            ``True`` if ``self`` is smaller than ``other``, ``False`` otherwise

        Examples:

            Check if a smaller program point is smaller than a larger one

            >>> smaller = ProgramPoint(["3.4.2026", "Point 1"])
            >>> larger = ProgramPoint(["4.4.2026", "Point 2"])
            >>> largest = ProgramPoint(["1.1.2027", "Point 3"])
            >>> smaller < larger
            True

            Sort some program points

            >>> sorted([larger, largest, smaller])
            [03.04.2026 Point 1, 04.04.2026 Point 2, 01.01.2027 Point 3]

        """

        if isinstance(other, ProgramPoint):
            if self.date < other.date:
                return True
            if self.date == other.date:
                return self.description < other.description

            return False

        return NotImplemented

    def __repr__(self):
        """Return a textual representation of the program point

        Examples:

            Print the representation of a simple program point

            >>> ProgramPoint(["1.1.1970", "Party"])
            01.01.1970 Party

        """

        return self.date.strftime("%d.%m.%Y") + f" {self.description}"

    def _unify_description(self) -> None:
        """Unify program point description

        Examples:

            Compare equal program points in different languages

            >>> (ProgramPoint(["6.10.2026", "Congress Day 1"]) ==
            ...  ProgramPoint(["6.10.2026", "1. Kongresstag"]))
            True

            Check the English description of a German program point

            >>> ProgramPoint(["11.5.2026", "Galadinner"])
            11.05.2026 Gala Dinner

        """

        self.description = sub(
            r"(\d+)\. Kongresstag", r"Congress Day \1", self.description
        )
        self.description = sub(r"Galadinner", "Gala Dinner", self.description)


# -- Grammar ------------------------------------------------------------------

weekday = (
    Keyword("Montag")
    | Keyword("Dienstag")
    | Keyword("Mittwoch")
    | Keyword("Donnerstag")
    | Keyword("Freitag")
    | Keyword("Samstag")
    | Keyword("Sonntag")
    | Keyword("Monday")
    | Keyword("Tuesday")
    | Keyword("Wednesday")
    | Keyword("Thursday")
    | Keyword("Friday")
    | Keyword("Saturday")
    | Keyword("Sunday")
)
integer = Word(nums)
date = Combine(integer + "." + integer + "." + integer).set_parse_action(
    lambda token: datetime.strptime(token[0], "%d.%m.%Y")
)
program_point_description = CharsNotIn(",\r\n").set_parse_action(strip)
program_point = (
    Suppress(Optional(weekday))
    + date
    + Suppress(Optional("-"))
    + program_point_description
).set_parse_action(ProgramPoint)

program_points = DelimitedList(program_point)
"""Program points

Example:

  Dienstag 6.10.2026 - Come Together,
  Mittwoch 7.10.2026 - 1. Kongresstag,
  Mittwoch 7.10.2026 - Galadinner,
  Donnerstag 8.10.2026 - 2. Kongresstag
"""

# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    from doctest import testmod

    testmod()
