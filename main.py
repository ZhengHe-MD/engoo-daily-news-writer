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
        description="Convert online articles to Engoo daily news format",
        prog="engoo-writer",
        epilog="Examples:\n"
               "  engoo-writer https://example.com/article\n"
               "  engoo-writer https://example.com/article -o lesson.html\n"
               "  engoo-writer https://example.com/article --gist\n"
               "  engoo-writer https://example.com/article --gist --description 'AI Ethics'",
        formatter_class=argparse.RawDescriptionHelpFormatter
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
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    # GitHub Gist options
    parser.add_argument("--gist", action="store_true", help="Share lesson via GitHub Gist")
    parser.add_argument("--update-gist", help="Update existing gist (provide gist ID)")
    parser.add_argument("--description", help="Custom description for the gist")
    
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    print(f"🔄 Converting article from: {args.url}")
    print("📚 Generating professional Engoo-style format...")
    
    # Convert the article
    result = convert_url_to_engoo(args.url)
    
    if result['success']:
        print("✅ Conversion successful!")
        article = result['article']
        
        print(f"📖 Title: {article['title']}")
        print(f"📝 Vocabulary: {len(article['vocabulary'])} items")
        print(f"💬 Discussion: {len(article['discussion_questions'])} questions")
        print(f"🤔 Further Discussion: {len(article['further_discussion_questions'])} questions")
        
        if args.output:
            save_to_file(result, args.output)
        else:
            # Default to HTML output
            default_output = "engoo_article.html"
            with open(default_output, 'w', encoding='utf-8') as f:
                f.write(article['html'])
            print(f"✅ Results saved to: {default_output}")
            args.output = default_output
            
        # Handle GitHub Gist sharing
        if args.gist or args.update_gist:
            try:
                from src.github_gist import create_shareable_lesson
                
                print("\n🌐 Sharing lesson via GitHub Gist...")
                
                gist_result = create_shareable_lesson(
                    html_content=result['article']['html'],
                    description=args.description,
                    gist_id=args.update_gist
                )
                
                print("✅ Lesson shared successfully!")
                print(f"🔗 Shareable link: {gist_result['preview_url']}")
                print(f"📝 Gist URL: {gist_result['gist_url']}")
                print(f"🆔 Gist ID: {gist_result['gist_id']}")
                print("\n💡 Share the 'Shareable link' with your students!")
                
                # Save gist info to a file for future reference
                output_name = args.output or "engoo_article.html"
                gist_info_file = output_name.replace('.html', '_gist_info.txt')
                with open(gist_info_file, 'w', encoding='utf-8') as f:
                    f.write(f"Gist ID: {gist_result['gist_id']}\n")
                    f.write(f"Shareable Link: {gist_result['preview_url']}\n")
                    f.write(f"Gist URL: {gist_result['gist_url']}\n")
                    f.write(f"Description: {gist_result['description']}\n")
                
                print(f"📄 Gist info saved to: {gist_info_file}")
                
            except ImportError:
                print("❌ GitHub Gist sharing requires 'requests' library. Install with: pip install requests")
            except ValueError as e:
                print(f"❌ GitHub configuration error: {e}")
                print("💡 Set your GITHUB_TOKEN environment variable to use gist sharing.")
                print("   Create a token at: https://github.com/settings/tokens")
            except Exception as e:
                print(f"❌ Failed to share via gist: {e}")
        else:
            if args.output and args.output.endswith('.html'):
                print(f"\n🌐 Local file: file://{Path(args.output).absolute()}")
                print("💡 Use --gist flag to share lesson online with students!")
            
    else:
        print(f"❌ Conversion failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
