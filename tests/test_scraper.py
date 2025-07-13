import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.scraper import WebScraper


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = WebScraper()
    
    def test_scraper_initialization(self):
        """Test scraper initialization."""
        self.assertIsNotNone(self.scraper.session)
        self.assertIn('User-Agent', self.scraper.session.headers)
    
    @patch('src.scraper.Article')
    def test_extract_article_content_success(self, mock_article_class):
        """Test successful article extraction."""
        # Mock Article instance
        mock_article = Mock()
        mock_article.title = "Test Title"
        mock_article.text = "Test content for the article."
        mock_article.authors = ["Author Name"]
        mock_article.publish_date = None
        mock_article_class.return_value = mock_article
        
        result = self.scraper.extract_article_content("https://example.com/article")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Title")
        self.assertEqual(result['text'], "Test content for the article.")
        self.assertEqual(result['url'], "https://example.com/article")
    
    @patch('src.scraper.Article')
    @patch('src.scraper.requests.Session.get')
    def test_extract_article_fallback(self, mock_get, mock_article_class):
        """Test fallback to manual scraping."""
        # Mock Article to fail
        mock_article = Mock()
        mock_article.title = ""
        mock_article.text = ""
        mock_article_class.return_value = mock_article
        
        # Mock requests response
        mock_response = Mock()
        mock_response.content = b"""
        <html>
            <head><title>Test Title</title></head>
            <body>
                <article>This is test content.</article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        result = self.scraper.extract_article_content("https://example.com/article")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], "Test Title")
        self.assertIn("This is test content.", result['text'])


if __name__ == '__main__':
    unittest.main()
