#!/bin/bash
# Pre-commit hook to run code quality checks

echo "Running pre-commit checks..."

# Run black formatter
echo "Running Black..."
black . --check
if [ $? -ne 0 ]; then
    echo "Black formatting check failed. Run 'black .' to fix."
    exit 1
fi

# Run isort
echo "Running isort..."
isort . --check-only
if [ $? -ne 0 ]; then
    echo "isort check failed. Run 'isort .' to fix."
    exit 1
fi

# Run flake8
echo "Running flake8..."
flake8
if [ $? -ne 0 ]; then
    echo "flake8 linting failed."
    exit 1
fi

# Run tests
echo "Running tests..."
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

echo "All checks passed!"
exit 0