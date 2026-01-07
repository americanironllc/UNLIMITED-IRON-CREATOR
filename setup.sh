#!/bin/bash
# Quick setup script for UNLIMITED IRON CREATOR

echo "🚀 UNLIMITED IRON CREATOR - Setup"
echo "=================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "✓ Python $PYTHON_VERSION detected"

# Create virtual environment (optional)
read -p "Create a virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
    echo "To activate it, run:"
    echo "  source venv/bin/activate  (Linux/Mac)"
    echo "  venv\\Scripts\\activate     (Windows)"
    echo ""
fi

# Create config from example
if [ ! -f config.json ]; then
    echo "Creating configuration file..."
    cp config.example.json config.json
    echo "✓ config.json created from example"
    echo "  Remember to add your API keys to config.json if using external AI services"
fi

# Create output directory
mkdir -p generated_media
echo "✓ Output directory created: generated_media/"

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo "=================================="
echo ""
echo "Quick start:"
echo "  python multimedia_generator.py text \"Your prompt here\""
echo "  python multimedia_generator.py image \"Your image description\""
echo "  python multimedia_generator.py project --config project_example.json"
echo ""
echo "For more information, see README.md"
