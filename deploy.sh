#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Print each command before executing it (for debugging purposes)
set -x

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Export Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install project dependencies
poetry install

# Run your main script
poetry run python main.py
