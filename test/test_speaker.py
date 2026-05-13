"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path

from wpkonverter.parsing.grammar.program_point import ProgramPoint
from wpkonverter.parsing.grammar.speaker import speaker_registration

# -- Tests --------------------------------------------------------------------


def test_speaker_registration1(checkers):
    """Try to parse first pre-registration data example"""

    filepath = Path(__file__).parent / "data" / "speaker1.txt"
    checkers.check_grammar(
        speaker_registration,
        filepath,
        {
            "Speaker": "Speaker Speaker, Prof.Dr.",
            "Organization": "TU Wien",
            "Position": "Head",
            "Mail Address": "speakerxcy001@speaker.com",
            "Telephone Number": "0123/456789",
            "Program Points": [
                ProgramPoint(["06.10.2026", "Come Together"]),
                ProgramPoint(["07.10.2026", "Congress Day 1"]),
                ProgramPoint(["07.10.2026", "Gala Dinner"]),
                ProgramPoint(["08.10.2026", "Congress Day 2"]),
            ],
            "Companion": True,
            "Name (Companion)": "Speaker+1 Speaker+1",
            "Organization (Companion)": "Nein",
            "Program Points (Companion)": [],
            "Message": "Hi, i want to go home.",
        },
    )


def test_speaker_registration2(checkers):
    """Try to parse second pre-registration data example"""

    filepath = Path(__file__).parent / "data" / "speaker2.txt"
    checkers.check_grammar(
        speaker_registration,
        filepath,
        {
            "Speaker": "TestSpeaker",
            "Organization": "Some Company",
            "Position": "",
            "Mail Address": "test.speaker@some.company.com",
            "Telephone Number": "+555 123",
            "Program Points": [ProgramPoint(["07.10.2026", "Congress Day 1"])],
            "Companion": False,
            "Name (Companion)": "Company Asset",
            "Organization (Companion)": "",
            "Program Points (Companion)": [
                ProgramPoint(["06.10.2026", "Come Together"])
            ],
            "Message": "This is speaker registration test data.",
        },
    )


def test_speaker_registration3(checkers):
    """Try to parse third pre-registration data example"""

    filepath = Path(__file__).parent / "data" / "speaker3.txt"
    checkers.check_grammar(
        speaker_registration,
        filepath,
        {
            "Speaker": "Speaker Test 1, BM",
            "Organization": "Test Uni",
            "Position": "BM",
            "Mail Address": "miksch@ift.at",
            "Telephone Number": "+43000000000",
            "Program Points": [
                ProgramPoint(["07.10.2026", "Congress Day 1"]),
                ProgramPoint(["07.10.2026", "Gala Dinner"]),
                ProgramPoint(["08.10.2026", "Congress Day 2"]),
            ],
            "Companion": True,
            "Name (Companion)": "Test 1 Begleitung",
            "Organization (Companion)": "Test Uni",
            "Program Points (Companion)": [
                ProgramPoint(["06.10.2026", "Come Together"]),
                ProgramPoint(["07.10.2026", "Gala Dinner"]),
            ],
            "Message": "kein Kommentar",
        },
    )
