"""Parsing support for pre-registration data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    contact_optional_number as contact,
    footer,
    footer_start,
    from_,
    message_start,
    organization,
    organization_start,
    position,
    participant_start,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

sponsor_start = Suppress(
    Keyword("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)

subject = between(subject_start, participant_start)
participant = between(participant_start, organization_start, "Participant")
sponsor = between(sponsor_start, message_start).set_parse_action(
    lambda tokens: tokens[0] != "nein"
)("Sponsor")
message = between(message_start, footer_start, "Message")

pre_registration = (
    from_
    + subject
    + participant
    + organization
    + position
    + contact
    + sponsor
    + message
    + footer_start
    + footer
)
