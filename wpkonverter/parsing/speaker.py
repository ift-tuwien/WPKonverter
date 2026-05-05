"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, SkipTo, Suppress, Word

from wpkonverter.parsing.common import (
    between,
    contact_start,
    from_,
    organization_start,
    subject_start,
    speaker_start,
    strip,
)

# -- Grammar ------------------------------------------------------------------

position_start = Suppress(Keyword("Position:"))
program_points_start = Suppress(
    Keyword("Ich nehme teil an folgenden Programmpunkten teil:")
)
companion_start = Suppress(Keyword("Begleitperson:"))
companion_organization_start = Suppress(
    Keyword("Unternehmen/Bildungsinstitut (wenn vorhanden):")
)
program_points_companion_start = Suppress(
    Keyword("Die Begleitperson nimmt an folgenden Programmpunkten  teil:")
)

subject = between(subject_start, speaker_start, "Subject")
speaker = between(speaker_start, organization_start, "Speaker")
organization = between(organization_start, position_start, "Organization")
position = between(position_start, contact_start, "Position")
contact = between(contact_start, program_points_start, "Contact")
program_points = between(
    program_points_start, companion_start, "Program Points"
)
companion_choice = Word("nein") ^ Word("ja")
companion = companion_start + companion_choice("Companion")
companion_name_text = SkipTo(companion_organization_start).set_parse_action(
    strip
)
companion_name = companion_name_text("Companion (Name)")
companion_organization = between(
    companion_organization_start,
    program_points_companion_start,
    "Organization (Companion)",
)

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
)
