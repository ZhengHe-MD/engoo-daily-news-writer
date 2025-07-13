<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Engoo Daily News Writer - Copilot Instructions

This project is an agentic system built with LangGraph that converts online articles into Engoo daily news format for ESL learners.

## Project Context
- **Purpose**: Convert blog posts and articles into structured ESL learning materials
- **Target Audience**: ESL teachers and intermediate English learners
- **AI Framework**: LangGraph for agentic workflows
- **AI Provider**: OpenAI GPT models for content processing

## Code Style and Standards
- Use type hints throughout the codebase
- Follow PEP 8 Python style guidelines
- Use dataclasses for data models when appropriate
- Include comprehensive docstrings for all classes and methods
- Handle exceptions gracefully with proper logging

## Architecture Guidelines
- **Modular Design**: Keep concerns separated (scraping, processing, agent orchestration)
- **Error Handling**: Implement robust error handling at each step
- **Logging**: Use structured logging for debugging and monitoring
- **Configuration**: Use environment variables for API keys and settings

## Key Components
1. **WebScraper**: Handles content extraction from URLs
2. **ContentProcessor**: AI-powered content transformation using OpenAI
3. **EngooNewsAgent**: LangGraph workflow orchestration
4. **Models**: Data structures for articles, vocabulary, and questions

## Engoo Format Requirements
- **Vocabulary**: 8-10 intermediate-level words with definitions and examples
- **Article**: 300-500 words, rewritten for intermediate ESL learners
- **Discussion**: 4-5 open-ended questions encouraging conversation
- **Further Discussion**: 3-4 advanced questions for deeper thinking

## Testing and Quality
- Write unit tests for core functionality
- Test with various article types and sources
- Validate AI-generated content quality
- Ensure proper error handling for edge cases

## Dependencies
- LangGraph for workflow management
- OpenAI for AI content processing
- BeautifulSoup/newspaper3k for web scraping
- Pydantic for data validation
