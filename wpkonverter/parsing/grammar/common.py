"""Common parsing functionality"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    Combine,
    Keyword,
    nums,
    Optional,
    ParserElement,
    ParseResults,
    printables,
    SkipTo,
    Suppress,
    Word,
)

# -- Functions ----------------------------------------------------------------


def strip(tokens: ParseResults) -> str:
    """Remove leading and trailing whitespace from input"""

    return tokens[0].strip()


def between(
    start: ParserElement,
    end: ParserElement,
    attribute: str | None = None,
):
    """Get parser element that parses text between two parser elements

    Args:

        start:

            The parser element that starts the text that should be parsed.

        end:

            The parser element that ends the text that should be parsed.

        attribute:

            The attribute (name) that stores the data between ``start`` and
            ``end``.

    Returns:

        A parser that consumes data between ``start`` (inclusive) and ``end``
        (exclusive) and stores the text between in the attribute ``attribute``.

    """

    text: ParserElement = SkipTo(end).set_parse_action(strip)
    if attribute is not None:
        text = text.set_results_name(attribute)
    return start + text


# -- Grammar ------------------------------------------------------------------

# ================
# = Start Tokens =
# ================

from_start = Suppress(Keyword("Von:") | Keyword("From:"))
subject_start = Suppress(Keyword("Betreff:") | Keyword("Subject:"))

participant_start = Suppress(
    Keyword("Teilnehmerin/Teilnehmer:") | Keyword("Participant:")
)
speaker_start = Suppress(
    Optional(Keyword("Speakerinnen/")) + Keyword("Speaker:")
)
sponsor_start = Suppress(Keyword("Sponsoren:"))

organization_start = Suppress(Keyword("Unternehmen/ Bildungsinstitut:"))
position_start = Suppress(Keyword("Position:"))
contact_start = Suppress(Keyword("Kontakt:"))
message_start = Suppress(Keyword("Nachricht:"))
footer_start = Suppress(Keyword("--"))
footer = Suppress(
    Keyword(
        "This is a notification that a contact form was submitted on your"
        " website (Wiener Produktionstechnik-Kongress"
    )
    + (
        Keyword("https://wpk.conf.tuwien.ac.at/en/).")
        | Keyword("https://wpk.conf.tuwien.ac.at).")
    )
)

# =================
# = General Rules =
# =================

from_ = between(from_start, subject_start)

mail_part = Word(printables, exclude_chars=",{}@")
contact_mail_text = Combine(mail_part + "@" + mail_part)
contact_mail = contact_start + contact_mail_text("Mail Address")
contact_telephone_number = Combine(Optional("+") + Word(nums + "/ "))
