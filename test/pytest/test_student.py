"""Test pre-registration grammar"""

# -- Imports ------------------------------------------------------------------

from wpkonverter.parsing.grammar.program_point import ProgramPoint
from wpkonverter.parsing.grammar.student import student_registration

# -- Tests --------------------------------------------------------------------


def test_student_registration1(checkers):
    """Try to parse first student registration data example"""

    checkers.check_grammar(
        student_registration,
        "student1.txt",
        {
            "Student": "Test Student",
            "Mail Address": "student@university.com",
            "Telephone Number": "+555 78",
            "University": "Tippydi Top University",
            "Student ID": "1337",
            "Program Points": [
                ProgramPoint(["6.10.2026", "Come Together"]),
            ],
            "Billing Address": "I Do Not Want To Pay Street 10",
            "VAT": "13234",
            "Billing Mode": "Post",
            "Billing Mail Address": "invoice@university.com",
            "Message": "This is\n\ntest\n\ndata",
        },
    )


def test_student_registration2(checkers):
    """Try to parse second student registration data example"""

    checkers.check_grammar(
        student_registration,
        "student2.txt",
        {
            "Student": "Student DE",
            "Student ID": "0123456789",
            "Mail Address": "student.de@test.com",
            "Telephone Number": "0123/456789",
            "University": "TU Wien",
            "Program Points": [
                ProgramPoint(["6.10.2026", "Come Together"]),
                ProgramPoint(["7.10.2026", "Congress Day 1"]),
                ProgramPoint(["8.10.2026", "Congress Day 2"]),
            ],
            "Billing Address": (
                "Getreidemarkt 9, Objekt 1, BA - OG 8 1060 Wien AUSTRIA"
            ),
            "VAT": "ATU 37675002",
            "Billing Mode": "Post",
            "Billing Mail Address": "wpk@ift.at",
            "Message": "",
        },
    )
