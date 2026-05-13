"""Parsing utilities"""

# -- Imports ------------------------------------------------------------------

from pyparsing import ParseResults

# -- Functions ----------------------------------------------------------------


def strip(tokens: ParseResults) -> str:
    """Remove leading and trailing whitespace from input"""

    return tokens[0].strip()
