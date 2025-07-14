# Engoo Daily News Writeo (Vibe-coded)

An agentic system built with LangGraph that converts online blog posts and articles into Engoo daily news format, perfect for ESL (English as a Second Language) teachers and students.

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

### Method 1: Direct Installation (Recommended)

1. Clone this repository:
```bash
git clone <repository-url>
cd engoo-daily-news-writer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the CLI executable:
```bash
chmod +x engoo-writer
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Method 2: Python Package Installation

```bash
# Install in development mode
pip install -e .

# Or install from source
pip install .
```

### Method 3: Using the executable

After installation, you can use the tool directly:
```bash
./engoo-writer "https://example.com/article"
```

Or if installed as a package:
```bash
engoo-writer "https://example.com/article"
```

4. (Optional) Set up GitHub token for gist sharing:
```bash
export GITHUB_TOKEN="your-github-token-here"
```

Create a GitHub Personal Access Token at https://github.com/settings/tokens with "gist" scope.

## Usage

### Command Line Interface

Convert an article from URL:
```bash
python main.py "https://example.com/article-url"
```

Save to a file:
```bash
# Save as text
python main.py "https://example.com/article-url" -o output.txt

# Save as HTML
python main.py "https://example.com/article-url" -o output.html

# Save as JSON
python main.py "https://example.com/article-url" -o output.json
```

Enable verbose logging:
```bash
python main.py "https://example.com/article-url" --verbose
```

### Easy HTML Generation and Sharing

For teachers who want to quickly generate and share professional HTML lessons:

```bash
# Generate HTML file locally (default behavior)
python main.py "https://example.com/article-url"

# Generate and share via GitHub Gist
python main.py "https://example.com/article-url" --gist --description "AI Ethics Lesson"

# Update an existing gist
python main.py "https://example.com/article-url" --update-gist GIST_ID

# Save to specific file and share
python main.py "https://example.com/article-url" -o my_lesson.html --gist
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
