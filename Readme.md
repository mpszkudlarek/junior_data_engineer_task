# Pandas Virtual Column

A recruitment task focused on adding a calculated column to a pandas DataFrame based on a string expression (e.g., `"col_a + col_b"`), with strict input validation.

## Setup & Run

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest test_virtual_column 1.py
