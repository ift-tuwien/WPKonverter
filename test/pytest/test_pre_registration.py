"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from wpkonverter.parsing.grammar.pre_registration import pre_registration

# -- Tests --------------------------------------------------------------------


def test_pre_registration1(checkers):
    """Check first example of pre-registration data"""

    checkers.check_grammar(
        pre_registration,
        "pre-registration1.txt",
        {
            "Participant": "Stefan Hinterberger",
            "Organization": "DEXIS Austria GmbH",
            "Position": "",
            "Mail Address": "stefan.hinterberger@dexis.at",
            "Telephone Number": "06646148120",
            "Sponsor": False,
            "Message": "",
        },
    )


def test_pre_registration2(checkers):
    """Check second example for pre-registration data"""

    checkers.check_grammar(
        pre_registration,
        "pre-registration2.txt",
        {
            "Participant": "Martin Leonhartsberger",
            "Organization": "Welser Profile",
            "Position": "Entwickler Mechatronik",
            "Mail Address": "ma.leonhartsberger@welser.com",
            "Telephone Number": "",
            "Sponsor": False,
            "Message": "",
        },
    )
