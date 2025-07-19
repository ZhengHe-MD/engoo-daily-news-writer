#!/bin/bash

# Create a release package for non-technical users
# This creates a clean, downloadable package with everything needed

set -e

PACKAGE_NAME="engoo-daily-news-writer-v1.0"
TEMP_DIR="/tmp/$PACKAGE_NAME"

echo "📦 Creating release package..."

# Clean up any existing temp directory
rm -rf "$TEMP_DIR"

# Create temp directory
mkdir -p "$TEMP_DIR"

# Copy essential files
cp -r src/ "$TEMP_DIR/"
cp requirements.txt "$TEMP_DIR/"
cp pyproject.toml "$TEMP_DIR/"
cp setup.py "$TEMP_DIR/"
cp main.py "$TEMP_DIR/"
cp engoo-writer "$TEMP_DIR/"
cp engoo_template.html "$TEMP_DIR/"
cp easy_install.sh "$TEMP_DIR/"
cp easy_install.bat "$TEMP_DIR/"
cp gui_launcher.py "$TEMP_DIR/"
cp README_EDUCATORS.md "$TEMP_DIR/"
cp .env.example "$TEMP_DIR/"

# Copy .gitignore but not .git directory
cp .gitignore "$TEMP_DIR/"

# Create a simple start script for GUI users
cat > "$TEMP_DIR/START_HERE.sh" << 'EOF'
#!/bin/bash

echo "🚀 Welcome to Engoo Daily News Writer!"
echo
echo "Choose how you'd like to run the setup:"
echo "1. Easy command-line setup (recommended)"
echo "2. Graphical interface (experimental)"
echo
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo "Running easy setup..."
        ./easy_install.sh
        ;;
    2)
        echo "Starting GUI launcher..."
        python3 gui_launcher.py
        ;;
    *)
        echo "Invalid choice. Please run ./easy_install.sh manually."
        ;;
esac
EOF

cat > "$TEMP_DIR/START_HERE.bat" << 'EOF'
@echo off
echo 🚀 Welcome to Engoo Daily News Writer!
echo.
echo Choose how you'd like to run the setup:
echo 1. Easy command-line setup (recommended)
echo 2. Graphical interface (experimental)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo Running easy setup...
    call easy_install.bat
) else if "%choice%"=="2" (
    echo Starting GUI launcher...
    python gui_launcher.py
) else (
    echo Invalid choice. Please run easy_install.bat manually.
    pause
)
EOF

# Make scripts executable
chmod +x "$TEMP_DIR/START_HERE.sh"
chmod +x "$TEMP_DIR/easy_install.sh"
chmod +x "$TEMP_DIR/gui_launcher.py"
chmod +x "$TEMP_DIR/engoo-writer"

# Create README for the package
cat > "$TEMP_DIR/README.md" << 'EOF'
# 📚 Engoo Daily News Writer - Easy Installation Package

Welcome! This package contains everything you need to start creating professional ESL lessons from any online article.

## 🚀 Quick Start

### For Mac/Linux Users:
```bash
./START_HERE.sh
```

### For Windows Users:
Double-click `START_HERE.bat`

### Alternative - Direct Setup:
- **Mac/Linux**: Run `./easy_install.sh`
- **Windows**: Run `easy_install.bat`

## 📖 What You Need

Before starting, you'll need two free accounts:

1. **OpenAI Account** (for AI processing)
   - Go to: https://platform.openai.com/api-keys
   - Create an account and get an API key

2. **GitHub Account** (for sharing lessons)
   - Go to: https://github.com/settings/tokens  
   - Create a personal access token with "gist" permission

## ✨ Features

- Convert any article to ESL lesson format
- Generate vocabulary with definitions
- Create discussion questions
- Share lessons online instantly
- Professional formatting

## 📞 Support

- Check `README_EDUCATORS.md` for detailed instructions
- Visit: https://github.com/ZhengHe-MD/engoo-daily-news-writer
- Report issues: https://github.com/ZhengHe-MD/engoo-daily-news-writer/issues

Happy teaching! 🎓✨
EOF

# Create the package
cd /tmp
echo "📁 Creating archive..."
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME/"
zip -r "$PACKAGE_NAME.zip" "$PACKAGE_NAME/" > /dev/null

echo "✅ Package created successfully!"
echo "📍 Location: /tmp/$PACKAGE_NAME.tar.gz"
echo "📍 Location: /tmp/$PACKAGE_NAME.zip"
echo
echo "📋 Package contents:"
ls -la "$TEMP_DIR/"

echo
echo "🎯 Ready for distribution!"
echo "Users can download either the .tar.gz (Mac/Linux) or .zip (Windows) file"
echo "and run START_HERE.sh or START_HERE.bat to begin."
