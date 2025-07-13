import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """Handles web scraping and content extraction from URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_article_content(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract article content from a given URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing title, text, and metadata
        """
        try:
            # Try using newspaper3k first
            article = Article(url)
            article.download()
            article.parse()
            
            if article.title and article.text:
                return {
                    'title': article.title,
                    'text': article.text,
                    'url': url,
                    'authors': article.authors,
                    'publish_date': article.publish_date,
                    'summary': article.summary if hasattr(article, 'summary') else None
                }
            
            # Fallback to manual scraping
            return self._manual_scrape(url)
            
        except Exception as e:
            logger.warning(f"Newspaper3k failed for {url}: {e}")
            return self._manual_scrape(url)
    
    def _manual_scrape(self, url: str) -> Optional[Dict[str, Any]]:
        """Fallback manual scraping method."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = None
            title_selectors = ['h1', 'title', '.title', '.headline', '.entry-title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    break
            
            # Extract article text
            text = None
            article_selectors = [
                'article', '.article', '.content', '.entry-content', 
                '.post-content', '.article-body', 'main', '.main'
            ]
            
            for selector in article_selectors:
                article_elem = soup.select_one(selector)
                if article_elem:
                    # Remove script and style elements
                    for script in article_elem(["script", "style"]):
                        script.decompose()
                    
                    # Get text
                    text = article_elem.get_text()
                    # Clean up whitespace
                    text = ' '.join(text.split())
                    break
            
            if title and text:
                return {
                    'title': title,
                    'text': text,
                    'url': url,
                    'authors': [],
                    'publish_date': None,
                    'summary': None
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Manual scraping failed for {url}: {e}")
            return None
