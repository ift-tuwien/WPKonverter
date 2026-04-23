"""Parsing support for WPK mail data"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    alphas,
    Group,
    LineEnd,
    Literal,
    nums,
    OneOrMore,
    ParserElement,
    Suppress,
    Word,
)

# -- Grammar ------------------------------------------------------------------

ParserElement.set_default_whitespace_chars(" \t")

newline = Suppress(LineEnd())
text = OneOrMore(Word(alphas + nums + " \t")).set_whitespace_chars("")

von = Suppress(Literal("Von:"))
from_ = von + Group(text) + newline
subject = Suppress(Literal("Betreff:"))
mail = from_ + subject

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
