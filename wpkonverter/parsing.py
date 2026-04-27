"""Parsing support for WPK mail data"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    Combine,
    Literal,
    OneOrMore,
    Regex,
    Suppress,
)

# -- Grammar ------------------------------------------------------------------


def rstrip(tokens):
    """Remove trailing whitespace from input"""

    return tokens[0].rstrip()


def strip(tokens):
    """Remove leading and trailing whitespace from input"""

    return tokens[0].strip()


char = Regex(r"[\s\S]")

from_start = Suppress(Literal("Von:"))
subject_start = Suppress(Literal("Betreff:"))
participant_start = Suppress(Literal("Teilnehmerin/Teilnehmer:"))
organization_start = Suppress(Literal("Unternehmen/ Bildungsinstitut:"))
contact_start = Suppress(Literal("Kontakt:"))
sponsor_start = Suppress(
    Literal("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)
message_start = Suppress(Literal("Nachricht:"))
end = Suppress(Literal("--"))
end_mail = Suppress(
    Literal(
        "This is a notification that a contact form was submitted on your"
        " website (Wiener Produktionstechnik-Kongress"
        " https://wpk.conf.tuwien.ac.at)."
    )
)


# ========
# = From =
# ========

text_from = Combine(OneOrMore(~subject_start + char)).set_parse_action(rstrip)
from_ = from_start + text_from

# ===========
# = Subject =
# ===========

text_subject = Combine(OneOrMore(~participant_start + char)).set_parse_action(
    rstrip
)
subject = subject_start + text_subject("subject")

# ===============
# = Participant =
# ===============

text_participant = Combine(
    OneOrMore(~organization_start + char)
).set_parse_action(rstrip)
participant = participant_start + text_participant("participant")

# ================
# = Organization =
# ================

text_organization = Combine(OneOrMore(~contact_start + char)).set_parse_action(
    rstrip
)
organization = organization_start + text_organization("organization")

# ===========
# = Contact =
# ===========

text_contact = Combine(OneOrMore(~sponsor_start + char)).set_parse_action(
    rstrip
)
contact = contact_start + text_contact("contact")

# ===========
# = Sponsor =
# ===========

text_sponsor = Combine(OneOrMore(~message_start + char)).set_parse_action(
    rstrip
)
sponsor = sponsor_start + text_sponsor("sponsor")

# ===========
# = Message =
# ===========

text_message = Combine(
    OneOrMore(~end + char).set_whitespace_chars(" \t")
).set_parse_action(strip)
message = message_start + text_message("message")

mail = (
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
mail_attributes = [
    "subject",
    "participant",
    "organization",
    "contact",
    "sponsor",
    "message",
]
