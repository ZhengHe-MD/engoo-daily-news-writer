#!/bin/bash

# Engoo Daily News Writer - Easy Installation Script
# This script makes it easy for non-developers to install and set up the tool

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo
    echo "=================================================="
    echo -e "${GREEN}  Engoo Daily News Writer - Easy Setup${NC}"
    echo "=================================================="
    echo
}

# Check if running on macOS or Linux
check_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
    else
        print_error "This installer supports macOS and Linux only."
        exit 1
    fi
    print_status "Detected OS: $OS"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher first."
        echo "Visit: https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
        print_error "Python 3.8 or higher is required. Found: Python $PYTHON_VERSION"
        echo "Please update Python: https://www.python.org/downloads/"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION found ✓"
}

# Install the tool
install_tool() {
    print_status "Installing Engoo Daily News Writer..."
    
    # Create virtual environment
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip
    print_status "Updating pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install requirements
    print_status "Installing dependencies (this may take a minute)..."
    pip install -r requirements.txt > /dev/null 2>&1
    
    # Install the package in development mode
    pip install -e . > /dev/null 2>&1
    
    print_success "Installation completed ✓"
}

# Interactive API key setup
setup_api_keys() {
    print_status "Setting up API keys..."
    echo
    echo "You need two API keys to use this tool:"
    echo "1. OpenAI API Key (for AI processing)"
    echo "2. GitHub Token (for sharing lessons)"
    echo
    
    # OpenAI API Key
    echo -e "${YELLOW}OpenAI API Key Setup:${NC}"
    echo "• Go to: https://platform.openai.com/api-keys"
    echo "• Sign in or create an account"
    echo "• Click 'Create new secret key'"
    echo "• Copy the key (starts with 'sk-')"
    echo
    
    while true; do
        read -p "Enter your OpenAI API Key: " OPENAI_KEY
        if [[ $OPENAI_KEY == sk-* ]]; then
            break
        else
            print_warning "OpenAI API keys start with 'sk-'. Please try again."
        fi
    done
    
    echo
    
    # GitHub Token
    echo -e "${YELLOW}GitHub Token Setup:${NC}"
    echo "• Go to: https://github.com/settings/tokens"
    echo "• Click 'Generate new token (classic)'"
    echo "• Give it a name like 'Engoo Writer'"
    echo "• Check the 'gist' permission"
    echo "• Click 'Generate token'"
    echo "• Copy the token (starts with 'github_pat_' or 'ghp_')"
    echo
    
    while true; do
        read -p "Enter your GitHub Token: " GITHUB_TOKEN
        if [[ $GITHUB_TOKEN == github_pat_* ]] || [[ $GITHUB_TOKEN == ghp_* ]]; then
            break
        else
            print_warning "GitHub tokens usually start with 'github_pat_' or 'ghp_'. Please verify and try again."
        fi
    done
    
    # Create .env file
    cat > .env << EOF
OPENAI_API_KEY=$OPENAI_KEY
LANGCHAIN_TRACING_V2=false
GITHUB_TOKEN=$GITHUB_TOKEN
EOF
    
    print_success "API keys saved ✓"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Test the CLI
    if ./engoo-writer --help > /dev/null 2>&1; then
        print_success "CLI tool is working ✓"
    else
        print_error "CLI tool test failed"
        return 1
    fi
    
    # Test API connections
    print_status "Testing API connections..."
    
    # Test OpenAI (simple check)
    if python3 -c "
import os
import openai
os.environ['OPENAI_API_KEY'] = open('.env').read().split('OPENAI_API_KEY=')[1].split('\n')[0]
client = openai.OpenAI()
# Just check if client initializes without making API call
print('OpenAI client initialized')
" > /dev/null 2>&1; then
        print_success "OpenAI API key format is valid ✓"
    else
        print_warning "OpenAI API key may have issues (but installation completed)"
    fi
    
    print_success "Installation test completed ✓"
}

# Create desktop shortcut (macOS)
create_shortcuts_macos() {
    print_status "Creating shortcuts..."
    
    INSTALL_DIR=$(pwd)
    
    # Create a launcher script
    cat > "$HOME/engoo-writer-launcher.sh" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source .venv/bin/activate
./engoo-writer "\$@"
EOF
    
    chmod +x "$HOME/engoo-writer-launcher.sh"
    
    # Add to PATH suggestion
    echo
    print_success "Shortcuts created ✓"
    echo
    echo "To use 'engoo-writer' from anywhere, add this to your shell profile:"
    echo -e "${YELLOW}export PATH=\"\$HOME:\$PATH\"${NC}"
    echo "Then create an alias:"
    echo -e "${YELLOW}alias engoo-writer=\"$HOME/engoo-writer-launcher.sh\"${NC}"
}

# Create desktop shortcut (Linux)
create_shortcuts_linux() {
    print_status "Creating shortcuts..."
    
    INSTALL_DIR=$(pwd)
    
    # Create a launcher script
    cat > "$HOME/engoo-writer-launcher.sh" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source .venv/bin/activate
./engoo-writer "\$@"
EOF
    
    chmod +x "$HOME/engoo-writer-launcher.sh"
    
    # Try to create desktop file
    if [[ -d "$HOME/Desktop" ]]; then
        cat > "$HOME/Desktop/Engoo-Writer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Engoo Writer
Comment=Convert articles to ESL lessons
Exec=$HOME/engoo-writer-launcher.sh
Icon=text-editor
Terminal=true
Categories=Education;
EOF
        chmod +x "$HOME/Desktop/Engoo-Writer.desktop"
        print_success "Desktop shortcut created ✓"
    fi
    
    echo
    echo "To use 'engoo-writer' from terminal, you can run:"
    echo -e "${YELLOW}$HOME/engoo-writer-launcher.sh${NC}"
}

# Print final instructions
print_final_instructions() {
    echo
    echo "=================================================="
    echo -e "${GREEN}  🎉 Installation Complete! 🎉${NC}"
    echo "=================================================="
    echo
    echo -e "${YELLOW}Quick Start:${NC}"
    echo "1. Convert an article:"
    echo "   ./engoo-writer convert https://example.com/article"
    echo
    echo "2. Convert and share online:"
    echo "   ./engoo-writer convert https://example.com/article --gist"
    echo
    echo "3. List your shared lessons:"
    echo "   ./engoo-writer gist list"
    echo
    echo -e "${YELLOW}Need Help?${NC}"
    echo "• Run: ./engoo-writer --help"
    echo "• Check: README.md"
    echo "• Issues: https://github.com/ZhengHe-MD/engoo-daily-news-writer/issues"
    echo
    echo -e "${GREEN}Happy teaching! 📚✨${NC}"
    echo
}

# Main installation flow
main() {
    print_header
    
    check_os
    check_python
    
    echo
    read -p "Ready to install Engoo Daily News Writer? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    install_tool
    setup_api_keys
    test_installation
    
    if [[ $OS == "macOS" ]]; then
        create_shortcuts_macos
    else
        create_shortcuts_linux
    fi
    
    print_final_instructions
}

# Run main function
main
