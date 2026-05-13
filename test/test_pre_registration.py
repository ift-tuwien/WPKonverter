"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path

from wpkonverter.parsing.grammar.pre_registration import pre_registration

# -- Tests --------------------------------------------------------------------


def test_pre_registration1(checkers):
    """Check first example of pre-registration data"""

    filepath = Path(__file__).parent / "data" / "pre-registration1.txt"
    checkers.check_grammar(
        pre_registration,
        filepath,
        {
            "Participant": "Stefan Hinterberger",
            "Organization": "DEXIS Austria GmbH",
            "Mail Address": "stefan.hinterberger@dexis.at",
            "Telephone Number": "06646148120",
            "Sponsor": "nein",
            "Message": "",
        },
    )
