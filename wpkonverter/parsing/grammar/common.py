"""Common parsing functionality"""

# -- Imports ------------------------------------------------------------------

from pyparsing import (
    Keyword,
    Optional,
    ParserElement,
    ParseResults,
    SkipTo,
    Suppress,
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

# ========
# = From =
# ========

from_ = between(from_start, subject_start)
