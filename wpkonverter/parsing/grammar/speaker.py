"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, Optional, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    contact_until_end,
    from_,
    organization,
    organization_start,
    position,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

speaker_start = Suppress(
    Optional(Keyword("Speakerinnen/")) + Keyword("Speaker:")
)

subject = between(subject_start, speaker_start)
speaker = between(speaker_start, organization_start, "Speaker")

speaker_registration = (
    from_ + subject + speaker + organization + position + contact_until_end
)
