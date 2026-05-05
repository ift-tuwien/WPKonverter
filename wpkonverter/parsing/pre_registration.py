"""Parsing support for pre-registration data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Suppress

from wpkonverter.parsing.common import (
    between,
    from_,
    organization_start,
    participant_start,
    strip,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

contact_start = Suppress(Keyword("Kontakt:"))
sponsor_start = Suppress(
    Keyword("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)
message_start = Suppress(Keyword("Nachricht:"))
end = Suppress(Keyword("--"))
end_mail = Suppress(
    Keyword(
        "This is a notification that a contact form was submitted on your"
        " website (Wiener Produktionstechnik-Kongress"
        " https://wpk.conf.tuwien.ac.at)."
    )
)

subject = between(subject_start, participant_start, "Subject", strip)
participant = between(
    participant_start, organization_start, "Participant", strip
)
organization = between(
    organization_start, contact_start, "Organization", strip
)
contact = between(contact_start, sponsor_start, "Contact", strip)
sponsor = between(sponsor_start, message_start, "Sponsor", strip)
message = between(message_start, end, "Message", strip)

pre_registration = (
    from_
    + subject
    + participant
    + organization
    + contact
    + sponsor
    + message
    + end
    + end_mail
)
