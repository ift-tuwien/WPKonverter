"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path

from wpkonverter.parsing.grammar.pre_registration import pre_registration

# -- Tests --------------------------------------------------------------------


def test_pre_registration(checkers):
    """Try to parse example pre-registration data"""

    filepath = Path(__file__).parent / "data" / "pre-registration.txt"
    checkers.check_grammar(
        pre_registration,
        filepath,
        {
            "Participant": "Stefan Hinterberger",
            "Organization": "DEXIS Austria GmbH",
            "Contact": "stefan.hinterberger@dexis.at\n06646148120",
            "Sponsor": "nein",
            "Message": "",
        },
    )
