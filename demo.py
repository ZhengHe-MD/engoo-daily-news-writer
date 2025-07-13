#!/usr/bin/env python3
"""
Demo script for the Engoo Daily News Writer
This script demonstrates how to use the system with a sample article.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src import convert_url_to_engoo


def demo_conversion():
    """Run a demo conversion with a sample article."""
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Sample URLs for testing (you can replace with any article URL)
    sample_urls = [
        "https://www.bbc.com/news",  # You can replace with any specific article
        "https://www.reuters.com",  # You can replace with any specific article
        "https://techcrunch.com",   # You can replace with any specific article
    ]
    
    print("🚀 Engoo Daily News Writer Demo")
    print("=" * 50)
    
    # Let user input a URL
    print("\nEnter an article URL to convert to Engoo format:")
    print("(Or press Enter to skip demo)")
    
    url = input("URL: ").strip()
    
    if not url:
        print("Demo skipped. You can run the conversion using:")
        print("python main.py 'your-article-url-here'")
        return
    
    print(f"\n🔄 Converting article from: {url}")
    print("This may take a moment while we:")
    print("  1. Scrape the article content")
    print("  2. Extract key vocabulary")
    print("  3. Rewrite for ESL learners")
    print("  4. Generate discussion questions")
    print("\nPlease wait...")
    
    try:
        result = convert_url_to_engoo(url)
        
        if result['success']:
            print("\n✅ Conversion successful!")
            article = result['article']
            
            print("\n" + "=" * 60)
            print(f"TITLE: {article['title']}")
            print("=" * 60)
            
            print(f"\n📚 VOCABULARY ({len(article['vocabulary'])} items):")
            for i, vocab in enumerate(article['vocabulary'][:3], 1):  # Show first 3
                print(f"{i}. {vocab['word']}: {vocab['definition']}")
                print(f"   Example: {vocab['example']}")
            if len(article['vocabulary']) > 3:
                print(f"   ... and {len(article['vocabulary']) - 3} more")
            
            print(f"\n📄 ARTICLE PREVIEW:")
            preview = article['article_body'][:400] + "..." if len(article['article_body']) > 400 else article['article_body']
            print(preview)
            
            print(f"\n💬 DISCUSSION QUESTIONS ({len(article['discussion_questions'])}):")
            for i, question in enumerate(article['discussion_questions'], 1):
                print(f"{i}. {question}")
            
            print(f"\n🤔 FURTHER DISCUSSION ({len(article['further_discussion_questions'])}):")
            for i, question in enumerate(article['further_discussion_questions'], 1):
                print(f"{i}. {question}")
            
            print("\n" + "=" * 60)
            print("🎉 Demo completed successfully!")
            print("\nTo save the full result, use:")
            print(f"python main.py '{url}' -o output.html")
            
        else:
            print(f"\n❌ Conversion failed: {result['error']}")
            print("\nPossible reasons:")
            print("- The URL might not contain a readable article")
            print("- The website might block automated access")
            print("- Network connectivity issues")
            print("- OpenAI API issues")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your internet connection and API key.")


if __name__ == "__main__":
    demo_conversion()
