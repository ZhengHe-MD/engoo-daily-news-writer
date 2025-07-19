# Engoo Daily News Writer

An agentic system built with LangGraph that converts online blog posts and articles into Engoo daily news format, perfect for ESL (English as a Second Language) teachers and students.

## 👥 For Different Users

### 🎓 **For Educators & Non-Technical Users**
Want to start creating lessons right away without technical setup? 

👉 **See [README_EDUCATORS.md](README_EDUCATORS.md)** for the easy, guided installation!

Features simple:
- ✅ One-click installation script
- ✅ Interactive API key setup 
- ✅ Graphical interface option
- ✅ Step-by-step instructions

### 👨‍💻 **For Developers & Technical Users**
Continue reading below for advanced setup, customization, and development details.

---

## Features

- **Web Scraping**: Automatically extracts content from any online article URL
- **AI-Powered Processing**: Uses OpenAI GPT models to:
  - Extract key vocabulary with definitions and examples
  - Rewrite articles for ESL learners (intermediate level)
  - Generate discussion questions
  - Create further discussion questions for advanced practice
- **LangGraph Workflow**: Implements a robust agentic system with error handling and validation
- **Multiple Output Formats**: Supports text, HTML, and JSON output formats
- **Easy Sharing**: Automatically share lessons via GitHub Gist with shareable links

## Engoo Daily News Format

The system generates content in the standard Engoo daily news format:

1. **Title**: Clear, engaging headline
2. **Vocabulary**: 8-10 key words with definitions and example sentences
3. **Article Body**: Rewritten for intermediate ESL learners (300-500 words)
4. **Discussion Questions**: 4-5 questions to encourage conversation
5. **Further Discussion**: 3-4 advanced questions for deeper thinking

## Installation

### 🚀 Easy Installation (Recommended for All Users)

**One-command setup for educators and non-technical users:**

```bash
# Clone the repository
git clone https://github.com/ZhengHe-MD/engoo-daily-news-writer.git
cd engoo-daily-news-writer

# Run the easy installer
./easy_install.sh          # Mac/Linux
# OR
easy_install.bat           # Windows
```

The easy installer will:
- ✅ Check your Python installation
- ✅ Set up a virtual environment
- ✅ Install all dependencies automatically
- ✅ Guide you through API key setup
- ✅ Test everything works
- ✅ Make the tool available globally

**What you need:**
- OpenAI API key (get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys))
- GitHub token (get from [github.com/settings/tokens](https://github.com/settings/tokens) with "gist" permission)

### 👨‍💻 Advanced Installation (For Developers)

#### Method 1: Manual Setup

1. Clone this repository:
```bash
git clone https://github.com/ZhengHe-MD/engoo-daily-news-writer.git
cd engoo-daily-news-writer
```

2. Create virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Make the CLI executable:
```bash
chmod +x engoo-writer
```

#### Method 2: Python Package Installation

```bash
# Install in development mode
pip install -e .

# Or install from source
pip install .
```

### 🎨 GUI Option (Experimental)

For users who prefer a graphical interface:

```bash
python3 gui_launcher.py
```

This provides a point-and-click interface for converting articles and managing lessons.

## Usage

### Quick Start (After Easy Installation)

**Basic Usage:**
```bash
# Convert any article from anywhere on your system
engoo-writer convert https://example.com/interesting-article

# Convert and share online instantly
engoo-writer convert https://example.com/article --gist

# List all your shared lessons
engoo-writer gist list

# Get help
engoo-writer --help
```

### Command Line Interface

**Convert Articles:**
```bash
# Basic conversion (creates HTML file)
engoo-writer convert https://example.com/article

# Save to specific file
engoo-writer convert https://example.com/article -o my-lesson.html

# Save as different formats
engoo-writer convert https://example.com/article -o lesson.txt  # Text format
engoo-writer convert https://example.com/article -o lesson.json # JSON format
```

**Share Lessons Online:**
```bash
# Convert and create shareable link
engoo-writer convert https://example.com/article --gist

# Manage your shared lessons
engoo-writer gist list          # List all lessons
engoo-writer gist get <id>      # View specific lesson
engoo-writer gist delete <id>   # Delete a lesson
```

**Debugging:**
```bash
# Enable verbose logging
engoo-writer convert https://example.com/article --verbose
```

### GitHub Gist Management

**Create and Share Lessons:**
```bash
# Create and share via GitHub Gist
engoo-writer convert https://example.com/article --gist

# Create with custom description
engoo-writer convert https://example.com/article --gist --description "AI Ethics Lesson"

# Update existing gist
engoo-writer convert https://example.com/article --update-gist GIST_ID
```

**Manage Your Gists:**
```bash
# List all your Engoo lesson gists
engoo-writer gist list

# List with limit
engoo-writer gist list --limit 5

# Get details of a specific gist
engoo-writer gist get GIST_ID

# Delete a gist (with confirmation)
engoo-writer gist delete GIST_ID

# Delete without confirmation
engoo-writer gist delete GIST_ID --confirm
```

The gist sharing feature:
- Creates a GitHub Gist with your lesson HTML
- Provides a shareable link that works immediately
- Allows easy updating of lessons
- Perfect for sharing with students or colleagues

### Python API

```python
from src import convert_url_to_engoo

# Convert an article
result = convert_url_to_engoo("https://example.com/article-url")

if result['success']:
    article = result['article']
    print(f"Title: {article['title']}")
    print(f"Vocabulary: {len(article['vocabulary'])} items")
    print(f"HTML: {article['html']}")
else:
    print(f"Error: {result['error']}")
```

## System Architecture

The system uses LangGraph to implement an agentic workflow:

1. **Scrape Content**: Extract article content from the provided URL
2. **Validate Content**: Ensure the content meets minimum requirements
3. **Process Content**: Use AI to transform content into Engoo format
4. **Finalize**: Package the results and handle any errors

### Components

- **WebScraper**: Handles content extraction using newspaper3k and BeautifulSoup
- **ContentProcessor**: AI-powered content transformation using OpenAI GPT
- **EngooNewsAgent**: LangGraph-based orchestration of the entire workflow
- **Models**: Data structures for vocabulary, questions, and articles

## Configuration

The system can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `GITHUB_TOKEN`: Your GitHub Personal Access Token for gist sharing (optional)

## Requirements

- Python 3.12+
- OpenAI API key
- Internet connection for web scraping and API calls

## Dependencies

- `langgraph`: Agentic workflow framework
- `openai`: OpenAI API client
- `beautifulsoup4`: HTML parsing for web scraping
- `requests`: HTTP client for web requests
- `newspaper3k`: Article extraction
- `pydantic`: Data validation and serialization
- `python-dotenv`: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Example Output

```
Title: NVIDIA Becomes First Company Valued at $4 Trillion

Vocabulary:
- trillion: A number equal to 1,000 billion (1,000,000,000,000)
- market capitalization: The total value of a company's shares
- artificial intelligence: Computer systems that can perform tasks typically requiring human intelligence
...

Article:
NVIDIA has become the first company in history to reach a market value of $4 trillion...

Discussion Questions:
1. What do you think makes NVIDIA so valuable?
2. How might artificial intelligence change our daily lives?
...

Further Discussion:
1. Do you think any company should be worth more than some countries' entire economies?
2. What are the potential risks of AI development happening so quickly?
...
```
