#!/usr/bin/env python3
"""
Simple test script to verify the Engoo Daily News Writer setup.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import openai
        import requests
        import bs4
        import langgraph
        import newspaper
        print("✅ All external packages imported successfully")
        
        # Test our modules
        import models
        import scraper
        import processor
        import agent
        
        from models import VocabularyItem, DiscussionQuestion, EngooArticle
        from scraper import WebScraper
        from processor import ContentProcessor
        from agent import EngooNewsAgent
        print("✅ All project modules imported successfully")
        
        # Test basic functionality
        vocab = VocabularyItem("innovation", "A new method or idea", "Innovation drives progress.")
        question = DiscussionQuestion("What do you think about innovation?")
        
        article = EngooArticle(
            title="Test Article",
            vocabulary=[vocab],
            article_body="This is a test article.",
            discussion_questions=[question],
            further_discussion_questions=[]
        )
        
        html = article.to_html()
        assert "Test Article" in html and "article-title" in html
        print("✅ Basic functionality test passed")
        
        # Test scraper initialization
        scraper = WebScraper()
        print("✅ WebScraper initialized successfully")
        
        print("\n🎉 All tests passed! The project is set up correctly.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-api-key-here'")
        print("2. Run the demo: python demo.py")
        print("3. Or convert an article: python main.py 'https://example.com/article'")
        print("4. Share via GitHub Gist: python main.py 'https://example.com/article' --gist")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
