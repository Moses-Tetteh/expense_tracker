#!/bin/bash
# Setup script for Expense Tracker development environment

set -e

echo "========================================="
echo "Expense Tracker - Development Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements-dev.txt

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created. Please update it with your settings."
else
    echo ".env file already exists."
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "Do you want to create a superuser? (y/n)"
read create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Generate test data
echo ""
echo "Do you want to generate test data? (y/n)"
read generate_data
if [ "$generate_data" = "y" ]; then
    python manage.py generate_test_data --users=3 --expenses=20
fi

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "To run tests, use:"
echo "  pytest"
echo ""
echo "For more information, see README.md"