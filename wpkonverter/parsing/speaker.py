"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Suppress

from wpkonverter.parsing.common import (
    between,
    contact_start,
    from_,
    organization_start,
    strip,
    subject_start,
    speaker_start,
)

# -- Grammar ------------------------------------------------------------------

position_start = Suppress(Keyword("Position:"))

subject = between(subject_start, speaker_start, "Subject", strip)
speaker = between(speaker_start, organization_start, "Speaker", strip)
organization = between(
    organization_start, position_start, "Organization", strip
)
position = between(position_start, contact_start, "Position", strip)

speaker_registration = from_ + subject + speaker + organization + position
