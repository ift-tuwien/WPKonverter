"""Parsing support for sponsor data"""

# -- Imports ------------------------------------------------------------------

from pyparsing import Keyword, Suppress

from wpkonverter.parsing.grammar.common import (
    between,
    contact_until_end,
    from_,
    organization,
    organization_start,
    subject_start,
)

# -- Grammar ------------------------------------------------------------------

sponsor_start = Suppress(Keyword("Sponsoren:"))

subject = between(subject_start, sponsor_start)
sponsor = between(sponsor_start, organization_start, "Sponsor")


sponsor_registration = (
    from_ + subject + sponsor + organization + contact_until_end
)
