"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from pathlib import Path

from wpkonverter.parsing.speaker import speaker_registration

# -- Tests --------------------------------------------------------------------


def test_pre_registration(checkers):
    """Try to parse example pre-registration data"""

    filepath = Path(__file__).parent / "data" / "speaker.txt"
    checkers.check_grammar(
        speaker_registration,
        filepath,
        {
            "Companion": "ja",
            "Companion (Name)": "Speaker+1 Speaker+1",
            "Mail Address": "speakerxcy001@speaker.com",
            "Message": "Hi, i want to go home.",
            "Organization": "TU Wien",
            "Organization (Companion)": "Nein",
            "Position": "Head",
            "Program Points": (
                "Dienstag 6.10.2026 - Come Together, Mittwoch 7.10.2026 - 1."
                " Kongresstag, Mittwoch 7.10.2026 - Galadinner, Donnerstag"
                " 8.10.2026 - 2. Kongresstag"
            ),
            "Program Points (Companion)": "",
            "Speaker": "Speaker Speaker, Prof.Dr.",
            "Subject": "Speaker Anmeldung WPK2026",
            "Telephone Number": "0123/456789",
        },
    )
