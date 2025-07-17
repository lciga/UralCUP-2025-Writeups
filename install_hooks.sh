#!/bin/bash
set -e

echo "Pre-commit installing..."

if ! command -v pre-commit &> /dev/null; then
    echo "Pre-commit not found. Install pre-commin via 'pip install pre-commit'"
    exit 1
fi

pre-commit install --install-hooks
echo "Pre-commit installed."
