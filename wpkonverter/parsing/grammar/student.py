"""Parsing support for student data"""

# -- Imports ------------------------------------------------------------------

from re import search

from pyparsing import Keyword, SkipTo, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    contact,
    contact_mail_text,
    from_,
    message_until_end,
    program_points,
    program_points_start,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

student_start = Suppress(Keyword("Studierende:") | Keyword("Participant:"))
university_start_de = Suppress(Keyword("Universitätsname:"))
university_start_en = Suppress(Keyword("University:"))
billing_address_start = Suppress(
    Keyword("Rechnungsadresse:") | Keyword("Billing address:")
)

subject = between(subject_start, student_start)
student = student_start + SkipTo("\n")("Student")

student_id_start = Suppress(
    Keyword("Matrikelnummer:") | Keyword("Student ID-number:")
)
student_id = student_id_start + SkipTo("\n")("Student ID")
# Unfortunately the order of information is different for the English and
# German version of the registration
university_de = between(
    university_start_de, program_points_start, "University"
)
university_en = university_start_en + SkipTo("\n")("University")
student_info_de = student_id + contact + university_de
student_info_en = contact + university_en + student_id

billing_address = billing_address_start + SkipTo("\n")("Billing Address")
vat = SkipTo("\n")("VAT")
billing_mode = SkipTo("\n").set_parse_action(
    lambda tokens: "Post" if search(r"[Pp]ost", tokens[0]) else "eMail"
)("Billing Mode")
billing_mail = contact_mail_text("Billing Mail Address")

student_registration = (
    from_
    + subject
    + student
    + (student_info_de | student_info_en)
    + program_points
    + billing_address
    + vat
    + billing_mode
    + billing_mail
    + message_until_end
)
