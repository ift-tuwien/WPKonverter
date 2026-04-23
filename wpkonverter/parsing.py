"""Parsing support for WPK mail data"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    Combine,
    LineEnd,
    Literal,
    OneOrMore,
    Regex,
    Suppress,
)

# -- Grammar ------------------------------------------------------------------

newline = Suppress(LineEnd())
char = Regex(r"[\s\S]")

subject_start = Suppress(Literal("Betreff:"))

text_from = Combine(OneOrMore(~subject_start + char))
from_start = Suppress(Literal("Von:"))

from_ = from_start + text_from

mail = from_

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
    print(result)


# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    main()
