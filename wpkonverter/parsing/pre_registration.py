"""Parsing support for pre-registration data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Combine, Keyword, SkipTo, Suppress

from wpkonverter.parsing.common import (
    from_,
    organization_start,
    participant_start,
    rstrip,
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

# ===========
# = Subject =
# ===========

text_subject = SkipTo(participant_start).set_parse_action(rstrip)
subject = subject_start + text_subject("Subject")

# ===============
# = Participant =
# ===============

text_participant = SkipTo(organization_start).set_parse_action(rstrip)
participant = participant_start + text_participant("Participant")

# ================
# = Organization =
# ================

text_organization = SkipTo(contact_start).set_parse_action(rstrip)
organization = organization_start + text_organization("Organization")

# ===========
# = Contact =
# ===========

text_contact = SkipTo(sponsor_start).set_parse_action(rstrip)
contact = contact_start + text_contact("Contact")

# ===========
# = Sponsor =
# ===========

text_sponsor = SkipTo(message_start).set_parse_action(rstrip)
sponsor = sponsor_start + text_sponsor("Sponsor")

# ===========
# = Message =
# ===========

text_message = Combine(SkipTo(end)).set_parse_action(strip)
message = message_start + text_message("Message")

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
