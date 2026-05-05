"""Parsing support for speaker data"""

# -- Imports ------------------------------------------------------------------


from pyparsing import Keyword, SkipTo, Suppress

from wpkonverter.parsing.common import (
    from_,
    organization_start,
    rstrip,
    subject_start,
    speaker_start,
)

# -- Grammar ------------------------------------------------------------------

position_start = Suppress(Keyword("Position:"))

# ===========
# = Subject =
# ===========

text_subject = SkipTo(speaker_start).set_parse_action(rstrip)
subject = subject_start + text_subject("Subject")

# ===========
# = Speaker =
# ===========

text_speaker = SkipTo(organization_start).set_parse_action(rstrip)
speaker = speaker_start + text_speaker("Speaker")

# ================
# = Organization =
# ================

text_organization = SkipTo(position_start).set_parse_action(rstrip)
organization = organization_start + text_organization("Organization")

# ===========
# = Grammar =
# ===========

speaker_registration = from_ + subject + speaker + organization
