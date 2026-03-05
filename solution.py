"""
Module providing a function to dynamically add calculated virtual columns
to a pandas DataFrame based on mathematical string expressions.
"""

import re

import pandas as pd

# Pre-compiled regular expressions for performance optimization:

# 1. Matches strings consisting entirely of letters and underscores.
#    Ensures no digits, hyphens, or other special characters are present.
_VALID_LABEL = re.compile(r"^[a-zA-Z_]+$")

# 2. Matches strings containing ONLY allowed rule characters:
#    letters, underscores, spaces, and the operators: +, *, -
_VALID_ROLE = re.compile(r"^[a-zA-Z_\s+*\-]+$")

# 3. Extracts sequences of letters and underscores.
#    Used to parse the mathematical rule and find individual column names.
_WORDS_RE = re.compile(r"[a-zA-Z_]+")


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Creates a new DataFrame with an additional column calculated based on a rule.
    Validates column names and the mathematical rule to ensure data integrity.
    """
    empty_df = pd.DataFrame([])

    # 1. Validate the new column name
    if not _VALID_LABEL.match(new_column):
        return empty_df

    # 2. Validate all existing columns
    if not all(_VALID_LABEL.match(str(col)) for col in df.columns):
        return empty_df

    # 3. Validate characters in the rule
    if not _VALID_ROLE.match(role):
        return empty_df

    # 4. Extract used columns from the rule and check their existence
    used_columns = _WORDS_RE.findall(role)
    if not used_columns or any(col not in df.columns for col in used_columns):
        return empty_df

    # 5. Safely evaluate the expression and assign the new column
    try:
        return df.assign(**{new_column: df.eval(role)})
    except (SyntaxError, ValueError, TypeError, KeyError, NameError):
        return empty_df
