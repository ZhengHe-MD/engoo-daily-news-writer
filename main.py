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
        prog="engoo-writer"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command (default)
    convert_parser = subparsers.add_parser('convert', help='Convert article to Engoo format')
    convert_parser.add_argument("url", help="URL of the article to convert")
    convert_parser.add_argument("-o", "--output", help="Output file path (supports .txt, .html, .json)", default=None)
    convert_parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    convert_parser.add_argument("--gist", action="store_true", help="Share lesson via GitHub Gist")
    convert_parser.add_argument("--update-gist", help="Update existing gist (provide gist ID)")
    convert_parser.add_argument("--description", help="Custom description for the gist")
    
    # Gist management commands
    gist_parser = subparsers.add_parser('gist', help='Manage GitHub Gists')
    gist_subparsers = gist_parser.add_subparsers(dest='gist_command', help='Gist operations')
    
    # List gists
    list_parser = gist_subparsers.add_parser('list', help='List all Engoo lesson gists')
    list_parser.add_argument('--limit', type=int, default=10, help='Maximum number of gists to show')
    
    # Delete gist
    delete_parser = gist_subparsers.add_parser('delete', help='Delete a specific gist')
    delete_parser.add_argument('gist_id', help='ID of the gist to delete')
    delete_parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompt')
    
    # Get gist details
    get_parser = gist_subparsers.add_parser('get', help='Get details of a specific gist')
    get_parser.add_argument('gist_id', help='ID of the gist to retrieve')
    
    # Global options
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    # If no command is provided, treat as convert with positional URL
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Handle legacy usage (direct URL without subcommand)
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and sys.argv[1] not in ['convert', 'gist']:
        # Insert 'convert' command for backward compatibility
        sys.argv.insert(1, 'convert')
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'convert':
        handle_convert_command(args)
    elif args.command == 'gist':
        handle_gist_command(args)
    else:
        parser.print_help()


def handle_convert_command(args):
    """Handle the convert command."""
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


def handle_gist_command(args):
    """Handle gist management commands."""
    if args.gist_command == 'list':
        handle_list_gists(args)
    elif args.gist_command == 'delete':
        handle_delete_gist(args)
    elif args.gist_command == 'get':
        handle_get_gist(args)
    else:
        print("❌ Please specify a gist command: list, delete, or get")
        sys.exit(1)


def handle_list_gists(args):
    """Handle listing gists."""
    try:
        from src.github_gist import GitHubGistClient
        
        print("📋 Listing your Engoo lesson gists...")
        client = GitHubGistClient()
        result = client.list_gists()
        
        if result['success']:
            gists = result['gists'][:args.limit]
            
            if not gists:
                print("📭 No Engoo lesson gists found.")
                print("💡 Create your first lesson with: engoo-writer convert <url> --gist")
                return
            
            print(f"\n📚 Found {result['total_count']} Engoo lesson gists:")
            print("-" * 80)
            
            for i, gist in enumerate(gists, 1):
                print(f"{i}. {gist['description']}")
                print(f"   🆔 ID: {gist['id']}")
                print(f"   � Created: {gist['created_at'][:10]}")
                print(f"   🔗 Preview: {gist['preview_url']}")
                print(f"   🌐 GitHub: {gist['html_url']}")
                print()
                
        else:
            print(f"❌ Failed to list gists: {result['error']}")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ GitHub configuration error: {e}")
        print("💡 Set your GITHUB_TOKEN environment variable to use gist management.")
        print("   Create a token at: https://github.com/settings/tokens")
        sys.exit(1)


def handle_delete_gist(args):
    """Handle deleting a gist."""
    try:
        from src.github_gist import GitHubGistClient
        
        client = GitHubGistClient()
        
        # First, get gist details to confirm
        gist_result = client.get_gist(args.gist_id)
        
        if not gist_result['success']:
            print(f"❌ Failed to find gist {args.gist_id}: {gist_result['error']}")
            sys.exit(1)
        
        gist = gist_result['gist']
        
        print(f"📋 Gist to delete:")
        print(f"   🆔 ID: {gist['id']}")
        print(f"   📝 Description: {gist['description']}")
        print(f"   📅 Created: {gist['created_at'][:10]}")
        print(f"   🔗 Preview: {gist['preview_url']}")
        
        if not args.confirm:
            response = input(f"\n⚠️  Are you sure you want to delete this gist? (y/N): ")
            if response.lower() != 'y':
                print("❌ Deletion cancelled.")
                return
        
        print(f"\n🗑️  Deleting gist {args.gist_id}...")
        result = client.delete_gist(args.gist_id)
        
        if result['success']:
            print("✅ Gist deleted successfully!")
        else:
            print(f"❌ Failed to delete gist: {result['error']}")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ GitHub configuration error: {e}")
        print("💡 Set your GITHUB_TOKEN environment variable to use gist management.")
        sys.exit(1)


def handle_get_gist(args):
    """Handle getting gist details."""
    try:
        from src.github_gist import GitHubGistClient
        
        client = GitHubGistClient()
        result = client.get_gist(args.gist_id)
        
        if result['success']:
            gist = result['gist']
            
            print(f"📋 Gist Details:")
            print(f"   🆔 ID: {gist['id']}")
            print(f"   📝 Description: {gist['description']}")
            print(f"   📅 Created: {gist['created_at'][:10]}")
            print(f"   🔄 Updated: {gist['updated_at'][:10]}")
            print(f"   🌍 Public: {'Yes' if gist['public'] else 'No'}")
            print(f"   📁 Files: {', '.join(gist['files'])}")
            print(f"   🔗 Preview: {gist['preview_url']}")
            print(f"   🌐 GitHub: {gist['html_url']}")
            
        else:
            print(f"❌ Failed to get gist: {result['error']}")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ GitHub configuration error: {e}")
        print("💡 Set your GITHUB_TOKEN environment variable to use gist management.")
        sys.exit(1)


if __name__ == "__main__":
    main()
