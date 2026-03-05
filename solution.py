"""
Module providing a function to dynamically add calculated virtual columns
to a pandas DataFrame based on mathematical string expressions.
"""

import re

import pandas as pd


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Creates a new DataFrame with an additional column calculated based on a rule.
    Validates column names and the mathematical rule to ensure data integrity.
    """
    empty_df = pd.DataFrame([])

    # 1. Validate the new column name (letters and underscores only)
    if not re.match(r"^[a-zA-Z_]+$", new_column):
        return empty_df

    # 2. Validate all existing columns (if ANY is invalid, return empty_df)
    if not all(re.match(r"^[a-zA-Z_]+$", str(col)) for col in df.columns):
        return empty_df

    # 3. Validate characters in the rule (letters, _, spaces, +, -, *)
    if not re.match(r"^[a-zA-Z_\s+*-]+$", role):
        return empty_df

    # 4. Extract used columns from the rule and check their existence
    used_columns = re.findall(r"[a-zA-Z_]+", role)
    if not used_columns or any(col not in df.columns for col in used_columns):
        return empty_df

    # 5. Safely evaluate the expression
    try:
        result_df = df.copy()
        result_df[new_column] = result_df.eval(role)
        return result_df
    except (SyntaxError, ValueError, TypeError, KeyError, NameError):
        return empty_df
