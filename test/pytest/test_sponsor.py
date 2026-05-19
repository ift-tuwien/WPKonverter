"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from wpkonverter.parsing.grammar.sponsor import sponsor_registration
from wpkonverter.parsing.grammar.program_point import ProgramPoint

# -- Tests --------------------------------------------------------------------


def test_sponsor_registration1(checkers):
    """Try to parse first sponsor registration data example"""

    checkers.check_grammar(
        sponsor_registration,
        "sponsor1.txt",
        {
            "Sponsor": "Test Sponsor",
            "Organization": "Some Company",
            "Mail Address": "someone@something.com",
            "Telephone Number": "+555 1234",
            "Program Points": [
                ProgramPoint(["07.10.2026", "Congress Day 1"]),
                ProgramPoint(["08.10.2026", "Congress Day 2"]),
            ],
            "Companion": False,
            "Name (Companion)": "Big Donor",
            "Organization (Companion)": "Some Company",
            "Program Points (Companion)": [
                ProgramPoint(["07.10.2026", "Gala Dinner"]),
            ],
            "Message": "This is\n\ntest data\n\nI am not a sponsor",
        },
    )
