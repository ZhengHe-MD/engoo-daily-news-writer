#!/usr/bin/env python3
"""
Engoo Daily News Writer
A command-line tool to convert online articles to Engoo daily news format.
"""

import argparse
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src import convert_url_to_engoo


def save_to_file(result: dict, output_file: str):
    """Save the conversion result to a file."""
    if result['success']:
        article = result['article']
        
        if output_file.endswith('.json'):
            # Save as JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        elif output_file.endswith('.html'):
            # Save as HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(article['html'])
        else:
            # Save as text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {article['title']}\n\n")
                
                f.write("Vocabulary:\n")
                for vocab in article['vocabulary']:
                    f.write(f"- {vocab['word']}: {vocab['definition']}\n")
                    f.write(f"  Example: {vocab['example']}\n")
                f.write("\n")
                
                f.write("Article:\n")
                f.write(article['article_body'])
                f.write("\n\n")
                
                f.write("Discussion Questions:\n")
                for i, question in enumerate(article['discussion_questions'], 1):
                    f.write(f"{i}. {question}\n")
                f.write("\n")
                
                f.write("Further Discussion:\n")
                for i, question in enumerate(article['further_discussion_questions'], 1):
                    f.write(f"{i}. {question}\n")
        
        print(f"Results saved to: {output_file}")
    else:
        print(f"Cannot save failed conversion: {result['error']}")


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert online articles to Engoo daily news format"
    )
    parser.add_argument(
        "url",
        help="URL of the article to convert"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (supports .txt, .html, .json)",
        default=None
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    print(f"Converting article from: {args.url}")
    print("This may take a moment...")
    
    # Convert the article
    result = convert_url_to_engoo(args.url)
    
    if result['success']:
        print("✅ Conversion successful!")
        article = result['article']
        
        print(f"\nTitle: {article['title']}")
        print(f"Vocabulary items: {len(article['vocabulary'])}")
        print(f"Discussion questions: {len(article['discussion_questions'])}")
        print(f"Further discussion questions: {len(article['further_discussion_questions'])}")
        
        if args.output:
            save_to_file(result, args.output)
        else:
            print("\nPreview:")
            print("-" * 50)
            print(article['title'])
            print("-" * 50)
            print(article['article_body'][:300] + "...")
            print("\nUse -o/--output to save the full result to a file.")
    else:
        print(f"❌ Conversion failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
