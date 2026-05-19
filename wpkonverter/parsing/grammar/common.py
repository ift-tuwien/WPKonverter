"""Common parsing functionality"""

# -- Imports ------------------------------------------------------------------

from re import search

from pyparsing import (
    Combine,
    Keyword,
    nums,
    Optional,
    ParserElement,
    ParseResults,
    printables,
    Regex,
    SkipTo,
    Suppress,
    Word,
)

from wpkonverter.parsing.grammar.program_point import (
    program_points as program_points_text,
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
sponsor_start = Suppress(Keyword("Sponsoren:"))
program_points_start = Suppress(
    Keyword("Ich nehme teil an folgenden Programmpunkten teil:")
    | Keyword("Veranstaltungen:")
    | Keyword("Events:")
)

organization_start = Suppress(Keyword("Unternehmen/ Bildungsinstitut:"))
position_start = Suppress(Keyword("Position:"))
contact_start = Suppress(Keyword("Kontakt:") | Keyword("Contact:"))
companion_start = Suppress(Keyword("Begleitperson:"))
companion_organization_start = Suppress(
    Keyword("Unternehmen/Bildungsinstitut (wenn vorhanden):")
)
companion_program_points_start = Suppress(
    Keyword("Die Begleitperson nimmt an folgenden Programmpunkten  teil:")
)

message_start = Suppress(Keyword("Nachricht:") | Keyword("Message:"))
footer_start = Suppress(Keyword("--"))
footer = Suppress(
    Keyword(
        "This is a notification that a contact form was submitted on your"
        " website (Wiener Produktionstechnik-Kongress"
    )
    + Regex(r"https://wpk\.conf\.tuwien\.ac\.at(?:/en/)?\)\.")
)

# =================
# = General Rules =
# =================

from_ = between(from_start, subject_start)

# Since the position seems to be optional we need to parse either to the start
# of the position or contact start token.
organization = between(
    organization_start, position_start | contact_start, "Organization"
)
position = Optional(between(position_start, contact_start)).set_parse_action(
    lambda tokens: "" if len(tokens) <= 0 else tokens[0]
)("Position")

mail_part = Word(printables, exclude_chars=",{}@")
contact_mail_text = Combine(mail_part + "@" + mail_part)
contact_mail = contact_start + contact_mail_text("Mail Address")
contact_telephone_number = Combine(Optional("+") + Word(nums + "/ "))

contact = contact_mail + contact_telephone_number("Telephone Number")
contact_optional_number = contact_mail + Optional(
    contact_telephone_number
).set_parse_action(lambda tokens: "" if len(tokens) <= 0 else tokens[0])(
    "Telephone Number"
)

program_points = program_points_start + program_points_text("Program Points")

# As far as I can tell the system adds the text `ja`, if you choose “yes”
# as answer to the question, if someone is accompanying you. For one mail,
# where I chose “no”, the system did not add text at all, while for another
# one it added `nein`.
companion_choice = Optional(Keyword("ja") | Keyword("nein"))
companion = (companion_start + companion_choice).set_parse_action(
    lambda tokens: False if len(tokens) <= 0 else tokens[0] == "ja"
)("Companion")
companion_name_text = SkipTo(companion_organization_start).set_parse_action(
    strip
)
companion_name = companion_name_text("Name (Companion)")
companion_organization = between(
    companion_organization_start,
    companion_program_points_start,
    "Organization (Companion)",
)
companion_program_points = (
    Suppress(companion_program_points_start) + Optional(program_points_text)
)("Program Points (Companion)")

billing_address_start = Suppress(
    Regex(r"Rechnungsadresse[:*]") | Regex(r"Billing [Aa]ddress[:*]")
)
billing_mode = SkipTo("\n").set_parse_action(
    lambda tokens: "Post" if search(r"[Pp]ost", tokens[0]) else "eMail"
)("Billing Mode")

message = between(message_start, footer_start, "Message")

companion_data = (
    companion
    + companion_name
    + companion_organization
    + companion_program_points
)

message_until_end = message + footer_start + footer
contact_until_end = (
    contact + program_points + companion_data + message_until_end
)
