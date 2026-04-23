"""Parsing support for WPK mail data"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    Combine,
    LineEnd,
    Literal,
    OneOrMore,
    Regex,
    StringEnd,
    Suppress,
)

# -- Grammar ------------------------------------------------------------------

newline = Suppress(LineEnd())
char = Regex(r"[\s\S]")
rstrip = lambda tokens: tokens[0].rstrip()

from_start = Suppress(Literal("Von:"))
subject_start = Suppress(Literal("Betreff:"))
participant_start = Suppress(Literal("Teilnehmerin/Teilnehmer:"))
organization_start = Suppress(Literal("Unternehmen/ Bildungsinstitut:"))
contact_start = Suppress(Literal("Kontakt:"))
sponsor_start = Suppress(
    Literal("Sind Sie daran interessiert, Sponsor oder Redner zu werden?:")
)
message_start = Suppress(Literal("Nachricht:"))
end = Suppress(Literal("""--
This is a notification that a contact form was submitted on your website (Wiener Produktionstechnik-Kongress https://wpk.conf.tuwien.ac.at).
"""))


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
subject = subject_start + text_subject

# ===============
# = Participant =
# ===============

text_participant = Combine(
    OneOrMore(~organization_start + char)
).set_parse_action(rstrip)
participant = participant_start + text_participant

# ================
# = Organization =
# ================

text_organization = Combine(OneOrMore(~contact_start + char)).set_parse_action(
    rstrip
)
organization = organization_start + text_organization

# ===========
# = Contact =
# ===========

text_contact = Combine(OneOrMore(~sponsor_start + char)).set_parse_action(
    rstrip
)
contact = contact_start + text_contact

# ===========
# = Sponsor =
# ===========

text_sponsor = Combine(OneOrMore(~message_start + char)).set_parse_action(
    rstrip
)
sponsor = sponsor_start + text_sponsor

# ===========
# = Message =
# ===========

text_message = Combine(OneOrMore(~end + char)).set_parse_action(rstrip)
message = message_start + text_message

mail = (
    from_
    + subject
    + participant
    + organization
    + contact
    + sponsor
    + message
    + end
    + StringEnd()
)

# -- Functions ----------------------------------------------------------------


def main() -> None:
    """Parse example pre-registration mail"""

    text = """\
Von: Website WPK24
Betreff: Vorregistrierung für WPK2026

Teilnehmerin/Teilnehmer: Thomas Trautner
Unternehmen/ Bildungsinstitut: TU Wien, Institut für Fertigungstechnik
Kontakt:
trautner@ift.at


Sind Sie daran interessiert, Sponsor oder Redner zu werden?: nein


Nachricht:
Ich freue mich auf die Teilnahme.

--
This is a notification that a contact form was submitted on your website \
(Wiener Produktionstechnik-Kongress https://wpk.conf.tuwien.ac.at).
    """

    print("—" * 20)
    print(text)
    print("—" * 20)

    result = mail.parse_string(text)
    print("Parsing Result:\n")
    print("—")
    for part in result:
        print(part)
        print("—")


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
