"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path

from wpkonverter.parsing.grammar.program_point import ProgramPoint
from wpkonverter.parsing.grammar.participant import participant_registration

# -- Tests --------------------------------------------------------------------


def test_participant_registration1(checkers):
    """Try to parse first participant registration data example"""

    filepath = Path(__file__).parent / "data" / "participant1.txt"
    checkers.check_grammar(
        participant_registration,
        filepath,
        {
            "Participant": "Teilnehmer DE",
            "Title": "MSc",
            "Organization": "TU Wien",
            "Position": "Assistent",
            "Mail Address": "teilnehmer.de@test.com",
            "Telephone Number": "0123/456789",
            "Program Points": [
                ProgramPoint(["6.10.2026", "Come Together"]),
                ProgramPoint(["7.10.2026", "Congress Day 1"]),
                ProgramPoint(["7.10.2026", "Gala Dinner"]),
                ProgramPoint(["8.10.2026", "Congress Day 2"]),
            ],
            "Billing Mode": "Post",
            "Companion": "Teilnehmerplus1 DE",
            "Organization (Companion)": "TU Wien",
            "Program Points (Companion)": [
                ProgramPoint(["6.10.2026", "Come Together"]),
                ProgramPoint(["7.10.2026", "Gala Dinner"]),
            ],
            "Billing Address": (
                "Getreidemarkt 9, Objekt 1, BA - OG 8 1060 Wien AUSTRIA"
            ),
            "VAT": "ATU 37675002",
            "Billing Mail Address": "wpk@ift.at",
            "Message": (
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed"
                " diam nonumy eirmod tempor invidunt ut labore et dolore magna"
                " aliquyam erat, sed diam voluptua. At vero eos et accusam et"
                " justo duo dolores et ea rebum. Stet clita kasd gubergren, no"
                " sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem"
                " ipsum dolor sit amet, consetetur sadipscing elitr, sed diam"
                " nonumy eirmod tempor invidunt ut labore et dolore magna"
                " aliquyam erat, sed diam voluptua. At vero eos et accusam et"
                " justo duo dolores et ea rebum. Stet clita kasd gubergren, no"
                " sea takimata sanctus est Lorem ipsum dolor sit amet."
            ),
        },
    )


def test_participant_registration2(checkers):
    """Try to parse second participant registration data example"""

    filepath = Path(__file__).parent / "data" / "participant2.txt"
    checkers.check_grammar(
        participant_registration,
        filepath,
        {
            "Participant": "High Priest Test Participant",
            "Title": "",
            "Organization": "Curch",
            "Position": "Top Mage",
            "Mail Address": "iam@mail.me",
            "Telephone Number": "+55 123",
            "Program Points": [
                ProgramPoint(["8.10.2026", "Congress Day 2"]),
            ],
            "Billing Mode": "eMail",
            "Companion": "Some One",
            "Organization (Companion)": "YoYo Institute",
            "Program Points (Companion)": [
                ProgramPoint(["6.10.2026", "Come Together"]),
            ],
            "Billing Address": "/dev/null",
            "VAT": "123",
            "Billing Mail Address": "hiho@mail.at",
            "Message": "This is test data",
        },
    )
