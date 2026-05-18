"""Parsing support for sponsor data"""

# -- Imports ------------------------------------------------------------------

from re import sub

from pyparsing import Keyword, Optional, SkipTo, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    billing_address_start,
    billing_mode,
    companion_organization,
    companion_program_points,
    companion_start,
    contact,
    from_,
    message_start,
    message_until_end,
    position,
    organization,
    participant_start,
    program_points,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

title_start = Suppress(Keyword("Titel:"))
vat_start = Suppress(Keyword("VAT number:") | Keyword("UID/VAT Nummer*"))
billing_mail_start = Suppress(
    Keyword("Rechnung:") | Keyword("Invoice e-mail:")
)

subject = between(subject_start, participant_start)
participant = participant_start + SkipTo("\n")("Participant")

title = Optional(title_start + SkipTo("\n")).set_parse_action(
    lambda tokens: "" if len(tokens) <= 0 else tokens[0]
)("Title")
# - According to the example data the information about the mode of billing
#   somehow ended up directly after the companion start token 😅
# - There is also a stray token `[second-name-begleitperson]` (probably a
#   incorrectly written variable of the template system) part of the English
#   version of the companion data 😢
companion = (
    companion_start
    + billing_mode
    + SkipTo("\n").set_parse_action((
        lambda tokens: (
            ""
            if len(tokens) <= 0
            else sub(r"\s*\[second-name-begleitperson\]\s*", " ", tokens[0])
        )
    ))("Companion")
)

# Unfortunately the billing format is different than the one used for students
billing_address = between(billing_address_start, vat_start, "Billing Address")
vat = between(vat_start, billing_mail_start, "VAT")
billing_mail = between(
    billing_mail_start, message_start, "Billing Mail Address"
)

participant_registration = (
    from_
    + subject
    + participant
    + title
    + organization
    + position
    + contact
    + program_points
    + companion
    + companion_organization
    + companion_program_points
    + billing_address
    + vat
    + billing_mail
    + message_until_end
)
