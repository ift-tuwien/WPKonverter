"""Parse program point information"""

# -- Imports ------------------------------------------------------------------

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

from wpkonverter.parsing.common import strip

# -- Classes ------------------------------------------------------------------


class ProgramPoint:
    """Store data about a single WPK program point"""

    def __init__(self, tokens):
        """Initialize the program point with the given tokens

        Args:

            tokens:

                The parsing tokens used to construct the program point

        """

        self.date = tokens[0]
        if len(tokens) >= 2:
            self.description = tokens[1]

    def __eq__(self, other):
        """Check if two program points are equal

        Examples:

            The same program points are equal

            >>> (ProgramPoint(["4.5.2006", "Dinner"]) ==
            ...  ProgramPoint(["4.5.2006", "Dinner"]))
            True

            Different program points are not equal

            >>> (ProgramPoint(["4.5.2006", "Dinner"]) ==
            ...  ProgramPoint(["4.5.2006", "Supper"]))
            False

        """

        if isinstance(other, ProgramPoint):
            return (
                self.date == other.date
                and self.description == other.description
            )

        return NotImplemented

    def __repr__(self):
        """Return a textual representation of the program point

        Examples:

            Print the representation of a simple program point

            >>> ProgramPoint(["1.1.1970", "Party"])
            1.1.1970 (Party)

        """

        representation = self.date
        if self.description is not None:
            representation += f" ({self.description})"

        return representation


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
date = Combine(integer + "." + integer + "." + integer)
program_point_description = CharsNotIn(",\r\n").set_parse_action(strip)
program_point = (
    Optional(Suppress(weekday))
    + date
    + Optional(Suppress("-"))
    + program_point_description
).set_parse_action(ProgramPoint)

program_points = DelimitedList(program_point).set_parse_action(
    lambda tokens: "\n".join(
        [f"• {program_point}" for program_point in map(repr, tokens)]
    )
)
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
