#!/bin/bash

# Personal Finance Coach - Code Linting Script
# This script runs various linting and formatting tools on the codebase

echo "🔍 Running code linting and formatting..."
echo "=========================================="

# Activate virtual environment
source venv/bin/activate

# Run import sorting
echo "📦 Organizing imports with isort..."
isort app/ run.py --profile=black --diff --check-only

# Run code formatting check
echo "🎨 Checking code formatting with Black..."
black --line-length=88 --diff --check app/ run.py

# Run style guide enforcement
echo "📏 Checking style guide compliance with flake8..."
flake8 app/ run.py

# Run comprehensive code analysis
echo "🔬 Running comprehensive analysis with pylint..."
pylint app/ run.py --fail-under=8.0

echo ""
echo "✅ Linting complete!"
echo ""
echo "To automatically fix formatting issues, run:"
echo "  source venv/bin/activate"
echo "  isort app/ run.py --profile=black"
echo "  black --line-length=88 app/ run.py"
echo "  autopep8 --in-place --aggressive --recursive app/ run.py"
