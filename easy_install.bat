@echo off
setlocal enabledelayedexpansion

:: Engoo Daily News Writer - Windows Easy Installation
:: This script makes it easy for non-developers to install and set up the tool on Windows

echo.
echo ==================================================
echo   Engoo Daily News Writer - Easy Setup
echo ==================================================
echo.

:: Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

:: Create virtual environment
echo [INFO] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Upgrade pip
echo [INFO] Updating pip...
python -m pip install --upgrade pip >nul 2>&1

:: Install requirements
echo [INFO] Installing dependencies (this may take a minute)...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

:: Install the package
pip install -e . >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install package
    pause
    exit /b 1
)

echo [SUCCESS] Installation completed

:: API Key Setup
echo.
echo [INFO] Setting up API keys...
echo.
echo You need two API keys to use this tool:
echo 1. OpenAI API Key (for AI processing)
echo 2. GitHub Token (for sharing lessons)
echo.

:: OpenAI API Key
echo OpenAI API Key Setup:
echo • Go to: https://platform.openai.com/api-keys
echo • Sign in or create an account
echo • Click 'Create new secret key'
echo • Copy the key (starts with 'sk-')
echo.

:ask_openai
set /p OPENAI_KEY="Enter your OpenAI API Key: "
if "%OPENAI_KEY:~0,3%" neq "sk-" (
    echo [WARNING] OpenAI API keys start with 'sk-'. Please try again.
    goto ask_openai
)

echo.

:: GitHub Token
echo GitHub Token Setup:
echo • Go to: https://github.com/settings/tokens
echo • Click 'Generate new token (classic)'
echo • Give it a name like 'Engoo Writer'
echo • Check the 'gist' permission
echo • Click 'Generate token'
echo • Copy the token
echo.

:ask_github
set /p GITHUB_TOKEN="Enter your GitHub Token: "
if "%GITHUB_TOKEN%" equ "" (
    echo [WARNING] Please enter a valid GitHub token.
    goto ask_github
)

:: Create .env file
echo OPENAI_API_KEY=%OPENAI_KEY%> .env
echo LANGCHAIN_TRACING_V2=false>> .env
echo GITHUB_TOKEN=%GITHUB_TOKEN%>> .env

echo [SUCCESS] API keys saved

:: Test installation
echo [INFO] Testing installation...
python main.py --help >nul 2>&1
if errorlevel 1 (
    echo [ERROR] CLI tool test failed
    pause
    exit /b 1
)

echo [SUCCESS] CLI tool is working

:: Create launcher script
echo @echo off> engoo-writer.bat
echo cd /d "%~dp0">> engoo-writer.bat
echo call .venv\Scripts\activate.bat>> engoo-writer.bat
echo python main.py %%*>> engoo-writer.bat

echo [SUCCESS] Launcher created

:: Final instructions
echo.
echo ==================================================
echo   🎉 Installation Complete! 🎉
echo ==================================================
echo.
echo Quick Start:
echo 1. Convert an article:
echo    engoo-writer.bat convert https://example.com/article
echo.
echo 2. Convert and share online:
echo    engoo-writer.bat convert https://example.com/article --gist
echo.
echo 3. List your shared lessons:
echo    engoo-writer.bat gist list
echo.
echo Need Help?
echo • Run: engoo-writer.bat --help
echo • Check: README_EDUCATORS.md
echo.
echo Happy teaching! 📚✨
echo.

pause
