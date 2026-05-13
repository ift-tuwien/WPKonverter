"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Optional, SkipTo, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    contact_mail,
    contact_telephone_number,
    footer,
    footer_start,
    from_,
    message_start,
    organization,
    organization_start,
    position,
    subject_start,
    speaker_start,
    strip,
)
from wpkonverter.parsing.grammar.program_point import (
    program_points as program_points_text,
)

# -- Grammar ------------------------------------------------------------------


program_points_start = Suppress(
    Keyword("Ich nehme teil an folgenden Programmpunkten teil:")
)
companion_start = Suppress(Keyword("Begleitperson:"))
companion_organization_start = Suppress(
    Keyword("Unternehmen/Bildungsinstitut (wenn vorhanden):")
)
companion_program_points_start = Suppress(
    Keyword("Die Begleitperson nimmt an folgenden Programmpunkten  teil:")
)

subject = between(subject_start, speaker_start)
speaker = between(speaker_start, organization_start, "Speaker")

contact = contact_mail + contact_telephone_number("Telephone Number")
program_points = program_points_start + program_points_text("Program Points")

# As far as I can tell the system only adds the text `ja`, if you choose
# “yes” as answer to the question, if someone is accompanying you. For the
# one mail, where I choose “no”, the system did not add text at all. I was
# still able to add information about a hypothetical person that was
# accompanying, which I did (for debugging purposes) although it is a
# nonsensical choice in this case.
companion_choice = Optional(Keyword("ja"))
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
message = between(message_start, footer_start, "Message")

speaker_registration = (
    from_
    + subject
    + speaker
    + organization
    + position
    + contact
    + program_points
    + companion
    + companion_name
    + companion_organization
    + companion_program_points
    + message
    + footer_start
    + footer
)
