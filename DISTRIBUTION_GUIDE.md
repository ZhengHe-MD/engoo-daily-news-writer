# 🎯 Engoo Daily News Writer - Distribution Guide

## For Non-Technical Users (Educators, Teachers, etc.)

This tool has been specifically designed to be accessible to educators and non-technical users who want to create professional ESL lessons without dealing with complex technical setup.

### 📦 Easy Installation Options

#### Option 1: One-Command Setup (Recommended)
```bash
# Mac/Linux users:
./easy_install.sh

# Windows users:
easy_install.bat
```

#### Option 2: Graphical Interface (Experimental)
```bash
python3 gui_launcher.py
```

#### Option 3: Step-by-Step Guide
See `README_EDUCATORS.md` for detailed, non-technical instructions.

### 🔑 What You Need

1. **OpenAI API Key** (free tier available)
   - Go to: https://platform.openai.com/api-keys
   - Create account → Generate API key
   - Copy the key (starts with `sk-`)

2. **GitHub Account** (free)
   - Go to: https://github.com/settings/tokens
   - Generate token → Select "gist" permission
   - Copy the token

### ✨ Key Benefits for Educators

- **No coding required** - Simple point-and-click interface
- **Professional output** - Generates properly formatted ESL lessons
- **Instant sharing** - Create shareable links for online teaching
- **Time-saving** - Convert any article in under 2 minutes
- **Customizable** - Edit generated content as needed

### 🎓 Perfect For

- ESL teachers creating lesson materials
- Language schools needing fresh content
- Online instructors sharing lessons with students
- Private tutors customizing materials
- Educational content creators

### 📱 How It Works

1. **Input**: Paste any article URL
2. **Process**: AI analyzes and converts the content
3. **Output**: Professional ESL lesson with:
   - Vocabulary list (8-10 words)
   - Simplified article text
   - Discussion questions
   - Advanced thinking questions
4. **Share**: Get instant online link to share with students

### 🔒 Privacy & Security

- All processing happens on your computer
- API keys stored locally only
- No data sent to third parties
- You control all generated content
- Delete shared lessons anytime

### 💡 Pro Tips

- **Best articles**: 500-2000 words work best
- **Content types**: News, blogs, opinion pieces are ideal
- **Student levels**: Output optimized for intermediate learners
- **Customization**: Generated HTML can be edited further

### 🆘 Getting Help

- Run with `--help` flag for command options
- Check `README_EDUCATORS.md` for detailed guide
- Report issues: https://github.com/ZhengHe-MD/engoo-daily-news-writer/issues

---

## For Technical Users & Developers

### 🛠 Advanced Setup

For developers who want to customize or extend the tool:

```bash
# Clone repository
git clone https://github.com/ZhengHe-MD/engoo-daily-news-writer.git
cd engoo-daily-news-writer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Test installation
./engoo-writer --help
```

### 🏗 Architecture

- **LangGraph**: Agentic workflow management
- **OpenAI GPT**: Content processing and generation
- **BeautifulSoup/newspaper3k**: Web scraping
- **GitHub API**: Gist sharing and management
- **Pydantic**: Data validation and models

### 🔧 Customization

Key files for customization:
- `src/models.py`: Data structures
- `src/processor.py`: AI prompts and processing logic
- `src/agent.py`: LangGraph workflow
- `engoo_template.html`: Output styling
- `main.py`: CLI interface

### 🧪 Testing & Development

```bash
# Run tests
python -m pytest tests/

# Test with sample article
./engoo-writer convert https://example.com/article

# Test gist functionality
./engoo-writer convert https://example.com/article --gist
./engoo-writer gist list
```

### 📊 Performance & Scaling

- **Processing time**: 30-60 seconds per article
- **API costs**: ~$0.01-0.05 per article (OpenAI pricing)
- **Rate limits**: Respects OpenAI API limits
- **Concurrent processing**: Single-threaded by design

### 🔄 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

### 📋 Dependencies

Core dependencies:
- `langgraph>=0.0.40`
- `openai>=1.0.0`
- `newspaper3k>=0.2.8`
- `beautifulsoup4>=4.12.0`
- `requests>=2.31.0`
- `pydantic>=2.0.0`

---

## 🚀 Distribution & Sharing

### Creating Release Packages

For maintainers distributing to non-technical users:

```bash
# Create distribution package
./create_release_package.sh

# This creates:
# - /tmp/engoo-daily-news-writer-v1.0.tar.gz (Mac/Linux)
# - /tmp/engoo-daily-news-writer-v1.0.zip (Windows)
```

Each package includes:
- ✅ All source code
- ✅ Easy installation scripts
- ✅ GUI launcher
- ✅ Documentation for educators
- ✅ Example configurations

### Package Contents

Users get a complete, self-contained package with:
- `START_HERE.sh` / `START_HERE.bat` - Entry point
- `easy_install.sh` / `easy_install.bat` - Automated setup
- `gui_launcher.py` - Graphical interface
- `README_EDUCATORS.md` - Non-technical guide
- All necessary source code and templates

### Recommended Distribution

1. **GitHub Releases**: Upload packages as release assets
2. **Documentation**: Link to `README_EDUCATORS.md` in release notes
3. **Support**: Direct users to GitHub Issues for help
4. **Updates**: Provide upgrade path in release notes

---

*This tool bridges the gap between advanced AI technology and practical classroom needs, making it easy for educators worldwide to create engaging, professional ESL content.*
