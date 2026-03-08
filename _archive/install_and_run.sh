#!/bin/bash

# Install dependencies and run LinkedIn Job Scraper

echo "========================================"
echo "  LinkedIn UK Job Scraper Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"
python3 --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]
then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Create output directory
echo ""
echo "📁 Creating output directory..."
mkdir -p output
echo "✓ Output directory ready"

# Run scraper
echo ""
echo "========================================"
echo "  Starting LinkedIn Job Scraper"
echo "========================================"
echo ""

python3 scraper.py "$@"
