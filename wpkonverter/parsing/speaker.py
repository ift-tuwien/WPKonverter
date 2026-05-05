"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Suppress

from wpkonverter.parsing.common import (
    between,
    contact_start,
    from_,
    organization_start,
    subject_start,
    speaker_start,
)

# -- Grammar ------------------------------------------------------------------

position_start = Suppress(Keyword("Position:"))

subject = between(subject_start, speaker_start, "Subject")
speaker = between(speaker_start, organization_start, "Speaker")
organization = between(organization_start, position_start, "Organization")
position = between(position_start, contact_start, "Position")

speaker_registration = from_ + subject + speaker + organization + position
