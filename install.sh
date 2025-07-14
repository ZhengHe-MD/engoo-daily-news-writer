#!/bin/bash
# Installation script for Engoo Daily News Writer

INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="engoo-writer"
CURRENT_DIR=$(pwd)

echo "🔧 Installing Engoo Daily News Writer CLI tool..."

# Check if running from the correct directory
if [[ ! -f "main.py" ]]; then
    echo "❌ Error: Please run this script from the engoo-daily-news-writer directory"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

# Create a wrapper script
cat > "$SCRIPT_NAME" << EOF
#!/bin/bash
cd "$CURRENT_DIR"
python3 main.py "\$@"
EOF

chmod +x "$SCRIPT_NAME"

# Copy to system PATH (requires sudo)
echo "📦 Installing to system PATH..."
if sudo cp "$SCRIPT_NAME" "$INSTALL_DIR/"; then
    echo "✅ Successfully installed $SCRIPT_NAME to $INSTALL_DIR"
    echo "🚀 You can now use 'engoo-writer' from anywhere!"
    echo ""
    echo "Usage examples:"
    echo "  engoo-writer https://example.com/article"
    echo "  engoo-writer https://example.com/article -o lesson.html"
    echo "  engoo-writer https://example.com/article --gist"
    echo ""
    echo "💡 Don't forget to set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
else
    echo "❌ Failed to install to system PATH"
    echo "💡 You can still use the local version: ./engoo-writer"
fi
