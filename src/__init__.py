import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_engoo_agent():
    """Create and configure the Engoo news agent."""
    try:
        from openai import OpenAI
        from .agent import EngooNewsAgent
        from .processor import ContentProcessor
        
        # Initialize OpenAI client
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        openai_client = OpenAI(api_key=openai_api_key)
        
        # Create content processor
        content_processor = ContentProcessor(openai_client)
        
        # Create and return agent
        return EngooNewsAgent(content_processor)
    except ImportError as e:
        logger.error(f"Import error: {e}")
        raise


def convert_url_to_engoo(url: str) -> dict:
    """
    Convert an article URL to Engoo daily news format.
    
    Args:
        url: The URL of the article to convert
        
    Returns:
        Dictionary containing the conversion result
    """
    try:
        agent = create_engoo_agent()
        result = agent.convert_article(url)
        return result
    except Exception as e:
        logger.error(f"Error converting URL {url}: {e}")
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }


if __name__ == "__main__":
    # Example usage
    example_url = "https://example.com/article"
    result = convert_url_to_engoo(example_url)
    
    if result['success']:
        print("Conversion successful!")
        print(f"Title: {result['article']['title']}")
        print(f"Vocabulary items: {len(result['article']['vocabulary'])}")
        print(f"Discussion questions: {len(result['article']['discussion_questions'])}")
    else:
        print(f"Conversion failed: {result['error']}")
