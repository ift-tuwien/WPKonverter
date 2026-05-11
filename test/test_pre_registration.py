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
            "Contact": "stefan.hinterberger@dexis.at\n06646148120",
            "Message": "",
            "Organization": "DEXIS Austria GmbH",
            "Participant": "Stefan Hinterberger",
            "Sponsor": "nein",
            "Subject": "Vorregistrierung für WPK2026",
        },
    )
