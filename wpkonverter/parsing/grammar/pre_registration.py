"""Parsing support for pre-registration data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Suppress

from wpkonverter.parsing.common import (
    between,
    contact_start,
    footer,
    footer_start,
    from_,
    message_start,
    organization_start,
    participant_start,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

sponsor_start = Suppress(
    Keyword("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)

subject = between(subject_start, participant_start, "Subject")
participant = between(participant_start, organization_start, "Participant")
organization = between(organization_start, contact_start, "Organization")
contact = between(contact_start, sponsor_start, "Contact")
sponsor = between(sponsor_start, message_start, "Sponsor")
message = between(message_start, footer_start, "Message")

pre_registration = (
    from_
    + subject
    + participant
    + organization
    + contact
    + sponsor
    + message
    + footer_start
    + footer
)
